/**
 * app.js —— SPA 路由、页面渲染、事件绑定
 * 依赖：js/api.js（全局 Api）
 * 路由：#/lessons  #/lessons/:id  #/exercises  #/exercises/:id  #/progress
 */
(function (global) {
  'use strict';

  var app = null;
  var currentToken = 0; // 防止快速切换路由时的异步结果覆盖新页面

  /* ==================== 通用工具 ==================== */

  function escapeHtml(value) {
    if (value === null || value === undefined) return '';
    return String(value)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  /** 轻量 Markdown 渲染：先转义全部文本，再解析 #/##、粗体、代码块、行内代码、列表 */
  function renderInline(raw) {
    var text = escapeHtml(raw);
    var codes = [];
    // 行内代码用占位符保护，避免其内部内容被粗体规则二次处理
    text = text.replace(/`([^`]+)`/g, function (match, code) {
      var token = '\u0000C' + codes.length + '\u0000';
      codes.push('<code>' + code + '</code>');
      return token;
    });
    text = text.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    text = text.replace(/(^|[^*])\*([^*]+)\*/g, '$1<em>$2</em>');
    text = text.replace(/\u0000C(\d+)\u0000/g, function (match, idx) {
      return codes[Number(idx)];
    });
    return text;
  }

  function renderMarkdown(src) {
    var lines = String(src == null ? '' : src).replace(/\r\n?/g, '\n').split('\n');
    var out = [];
    var paragraph = [];
    var i = 0;

    function flushParagraph() {
      if (paragraph.length) {
        out.push('<p>' + paragraph.map(renderInline).join('<br>') + '</p>');
        paragraph = [];
      }
    }

    while (i < lines.length) {
      var line = lines[i];

      // 围栏代码块 ```
      var fence = line.match(/^\s*```\s*([^`]*)\s*$/);
      if (fence) {
        flushParagraph();
        var lang = (fence[1] || '').trim().replace(/[^\w+-]/g, '');
        var codeLines = [];
        i += 1;
        while (i < lines.length && !/^\s*```\s*$/.test(lines[i])) {
          codeLines.push(lines[i]);
          i += 1;
        }
        if (i < lines.length) i += 1; // 跳过结束围栏
        var cls = lang ? ' class="language-' + escapeHtml(lang) + '"' : '';
        out.push('<pre><code' + cls + '>' + escapeHtml(codeLines.join('\n')) + '</code></pre>');
        continue;
      }

      // 标题 # ~ ######
      var heading = line.match(/^\s*(#{1,6})\s+(.*)$/);
      if (heading) {
        flushParagraph();
        var level = heading[1].length;
        out.push('<h' + level + '>' + renderInline(heading[2]) + '</h' + level + '>');
        i += 1;
        continue;
      }

      // 无序列表 - / * / +
      if (/^\s*[-*+]\s+/.test(line)) {
        flushParagraph();
        var items = [];
        while (i < lines.length && /^\s*[-*+]\s+/.test(lines[i])) {
          items.push('<li>' + renderInline(lines[i].replace(/^\s*[-*+]\s+/, '')) + '</li>');
          i += 1;
        }
        out.push('<ul>' + items.join('') + '</ul>');
        continue;
      }

      // 有序列表 1.
      var olMatch = line.match(/^\s*\d+\.\s+(.*)$/);
      if (olMatch) {
        flushParagraph();
        var olItems = [];
        while (i < lines.length) {
          var m = lines[i].match(/^\s*\d+\.\s+(.*)$/);
          if (!m) break;
          olItems.push('<li>' + renderInline(m[1]) + '</li>');
          i += 1;
        }
        out.push('<ol>' + olItems.join('') + '</ol>');
        continue;
      }

      // 空行
      if (/^\s*$/.test(line)) {
        flushParagraph();
        i += 1;
        continue;
      }

      paragraph.push(line.trim());
      i += 1;
    }
    flushParagraph();
    return out.join('\n');
  }

  var toastEl = null;
  function toast(message, type) {
    if (!toastEl) toastEl = document.getElementById('toast');
    if (!toastEl) return;
    toastEl.textContent = message;
    toastEl.className = 'toast show' + (type ? ' toast-' + type : '');
    clearTimeout(toastEl._timer);
    toastEl._timer = setTimeout(function () { toastEl.className = 'toast'; }, 2600);
  }

  function copyText(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(text);
    }
    // file:// 等非安全上下文的降级方案
    return new Promise(function (resolve, reject) {
      var ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      try {
        var ok = document.execCommand('copy');
        document.body.removeChild(ta);
        if (ok) resolve(); else reject(new Error('copy failed'));
      } catch (e) {
        document.body.removeChild(ta);
        reject(e);
      }
    });
  }

  function bindCopyButtons() {
    var buttons = app.querySelectorAll('.copy-btn');
    Array.prototype.forEach.call(buttons, function (btn) {
      btn.addEventListener('click', function () {
        copyText(btn.getAttribute('data-code') || '').then(function () {
          var old = btn.textContent;
          btn.textContent = '已复制 ✓';
          setTimeout(function () { btn.textContent = old; }, 1500);
        }).catch(function () {
          toast('复制失败，请手动选择代码', 'error');
        });
      });
    });
  }

  /* ==================== 页面片段 ==================== */

  function pageHeader(title, subtitle) {
    return '<div class="page-header"><div>' +
      '<h1 class="page-title">' + escapeHtml(title) + '</h1>' +
      (subtitle ? '<p class="page-subtitle">' + escapeHtml(subtitle) + '</p>' : '') +
      '</div></div>';
  }

  function setLoading() {
    var cards = '';
    for (var i = 0; i < 6; i++) cards += '<div class="skeleton-card"></div>';
    app.innerHTML = '<div class="page"><div class="skeleton-grid">' + cards + '</div></div>';
  }

  function setError(message, retryFn) {
    app.innerHTML = '<div class="page"><div class="state state-error">' +
      '<div class="state-icon">!</div>' +
      '<h2>加载失败</h2>' +
      '<p>' + escapeHtml(message) + '</p>' +
      '<button class="btn btn-primary" id="retryBtn" type="button">重试</button>' +
      '</div></div>';
    var btn = document.getElementById('retryBtn');
    if (btn && retryFn) {
      btn.addEventListener('click', retryFn);
    }
  }

  function emptyState(text) {
    return '<div class="state"><div class="state-icon" style="background:#f0edff;color:#6c5ce7">∅</div>' +
      '<h2>' + escapeHtml(text) + '</h2><p>稍后再来看看吧</p></div>';
  }

  function codeBlock(code) {
    return '<div class="code-block">' +
      '<div class="code-head"><span class="code-lang">Python</span>' +
      '<button class="copy-btn" type="button" data-code="' + escapeHtml(code) + '">复制代码</button>' +
      '</div><pre><code>' + escapeHtml(code) + '</code></pre></div>';
  }

  function difficultyInfo(d) {
    var map = {
      easy: { label: '简单', cls: 'diff-easy' },
      medium: { label: '中等', cls: 'diff-medium' },
      hard: { label: '困难', cls: 'diff-hard' }
    };
    return map[d] || { label: d || '未知', cls: 'diff-easy' };
  }

  function percentOf(part, total) {
    if (!total || total <= 0) return 0;
    return Math.round((part / total) * 100);
  }

  function isCurrent(token) { return token === currentToken; }

  /* ==================== 视图 1：教程列表 ==================== */

  function viewLessons() {
    var token = currentToken;
    setLoading();
    Api.getLessons().then(function (lessons) {
      if (!isCurrent(token)) return;
      if (!Array.isArray(lessons) || !lessons.length) {
        app.innerHTML = '<div class="page">' + pageHeader('基础语法教程', '从零开始掌握 Python 核心语法') +
          emptyState('暂无教程内容') + '</div>';
        return;
      }
      var cards = lessons.map(function (l) {
        return '<a class="card lesson-card" href="#/lessons/' + encodeURIComponent(l.id) + '">' +
          '<div class="card-top">' +
            '<span class="order-badge">第 ' + escapeHtml(l.order_index) + ' 课</span>' +
            '<span class="duration">' + escapeHtml(l.duration_min) + ' 分钟</span>' +
          '</div>' +
          '<h3 class="card-title">' + escapeHtml(l.title) + '</h3>' +
          '<p class="card-summary">' + escapeHtml(l.summary || '') + '</p>' +
          '<span class="card-link">查看详情 →</span>' +
        '</a>';
      }).join('');
      app.innerHTML = '<div class="page">' +
        pageHeader('基础语法教程', '从零开始掌握 Python 核心语法，按顺序学习效果更佳') +
        '<div class="card-grid">' + cards + '</div></div>';
    }).catch(function (err) {
      if (isCurrent(token)) setError(Api.friendlyMessage(err), viewLessons);
    });
  }

  /* ==================== 视图 2：教程详情 ==================== */

  function viewLessonDetail(id) {
    var token = currentToken;
    setLoading();
    Api.getLesson(id).then(function (lesson) {
      if (!isCurrent(token)) return;

      var exercisesHtml = '';
      if (Array.isArray(lesson.exercise_ids) && lesson.exercise_ids.length) {
        exercisesHtml = '<section class="section"><h2 class="section-title">配套练习</h2>' +
          '<div class="chip-row">' +
          lesson.exercise_ids.map(function (eid) {
            return '<a class="chip" href="#/exercises/' + encodeURIComponent(eid) +
              '">练习 #' + escapeHtml(eid) + ' →</a>';
          }).join('') +
          '</div></section>';
      }

      app.innerHTML = '<div class="page detail-page">' +
        '<a class="back-link" href="#/lessons">← 返回教程列表</a>' +
        pageHeader(lesson.title, '第 ' + escapeHtml(lesson.order_index) + ' 课 · ' +
          escapeHtml(lesson.duration_min) + ' 分钟') +
        (lesson.summary ? '<p class="lead">' + escapeHtml(lesson.summary) + '</p>' : '') +
        '<section class="section"><h2 class="section-title">教程内容</h2>' +
          '<div class="markdown">' + renderMarkdown(lesson.content_md) + '</div>' +
        '</section>' +
        (lesson.code_example ? '<section class="section"><h2 class="section-title">示例代码</h2>' +
          codeBlock(lesson.code_example) + '</section>' : '') +
        exercisesHtml +
        '<div class="detail-actions">' +
          '<button class="btn btn-primary btn-lg" id="markLessonBtn" type="button">标记已学完</button>' +
        '</div>' +
      '</div>';

      bindCopyButtons();

      var markBtn = document.getElementById('markLessonBtn');
      markBtn.addEventListener('click', function () {
        markBtn.disabled = true;
        var original = markBtn.textContent;
        markBtn.textContent = '提交中…';
        Api.markLesson(id).then(function () {
          markBtn.textContent = '✓ 已学完';
          markBtn.className = 'btn btn-success btn-lg';
          toast('已标记为学完', 'success');
        }).catch(function (err) {
          markBtn.disabled = false;
          markBtn.textContent = original;
          toast(Api.friendlyMessage(err), 'error');
        });
      });
    }).catch(function (err) {
      if (isCurrent(token)) setError(Api.friendlyMessage(err), function () { viewLessonDetail(id); });
    });
  }

  /* ==================== 视图 3：练习列表 ==================== */

  function viewExercises() {
    var token = currentToken;
    setLoading();
    Promise.all([Api.getExercises(), Api.getLessons()]).then(function (results) {
      if (!isCurrent(token)) return;
      var exercises = results[0] || [];
      var lessons = results[1] || [];
      var lessonMap = {};
      lessons.forEach(function (l) { lessonMap[l.id] = l.title; });

      if (!Array.isArray(exercises) || !exercises.length) {
        app.innerHTML = '<div class="page">' + pageHeader('练习题', '通过练习巩固所学知识') +
          emptyState('暂无练习题') + '</div>';
        return;
      }

      var cards = exercises.map(function (ex) {
        var diff = difficultyInfo(ex.difficulty);
        return '<a class="card exercise-card" href="#/exercises/' + encodeURIComponent(ex.id) + '">' +
          '<div class="card-top">' +
            '<span class="order-badge">练习 ' + escapeHtml(ex.order_index) + '</span>' +
            '<span class="difficulty ' + diff.cls + '">' + diff.label + '</span>' +
          '</div>' +
          '<h3 class="card-title">' + escapeHtml(ex.title) + '</h3>' +
          '<p class="card-meta">所属教程：' +
            escapeHtml(lessonMap[ex.lesson_id] || ('教程 #' + ex.lesson_id)) + '</p>' +
          '<span class="card-link">去作答 →</span>' +
        '</a>';
      }).join('');
      app.innerHTML = '<div class="page">' +
        pageHeader('练习题', '通过练习巩固所学知识') +
        '<div class="card-grid">' + cards + '</div></div>';
    }).catch(function (err) {
      if (isCurrent(token)) setError(Api.friendlyMessage(err), viewExercises);
    });
  }

  /* ==================== 视图 4：答题页 ==================== */

  function viewExerciseDetail(id) {
    var token = currentToken;
    setLoading();
    Api.getExercise(id).then(function (ex) {
      if (!isCurrent(token)) return;
      var diff = difficultyInfo(ex.difficulty);
      var starter = ex.starter_code || '';

      app.innerHTML = '<div class="page detail-page">' +
        '<a class="back-link" href="#/exercises">← 返回练习列表</a>' +
        pageHeader(ex.title, '难度：' + diff.label) +
        '<section class="section"><h2 class="section-title">题目描述</h2>' +
          '<div class="description">' + escapeHtml(ex.description || '').replace(/\n/g, '<br>') + '</div>' +
        '</section>' +
        '<section class="section">' +
          '<div class="editor-head"><h2 class="section-title">代码编辑器</h2>' +
          '<button class="btn btn-ghost btn-sm" id="resetCodeBtn" type="button">重置代码</button></div>' +
          '<textarea id="codeEditor" class="code-editor" spellcheck="false" ' +
            'autocapitalize="off" autocomplete="off" aria-label="代码输入框">' +
            escapeHtml(starter) + '</textarea>' +
          '<div class="editor-actions">' +
            '<button class="btn btn-primary btn-lg" id="submitCodeBtn" type="button">提交代码</button>' +
          '</div>' +
          '<div id="submitResult" class="submit-result" hidden></div>' +
        '</section>' +
      '</div>';

      var editor = document.getElementById('codeEditor');
      var submitBtn = document.getElementById('submitCodeBtn');
      var resetBtn = document.getElementById('resetCodeBtn');
      var resultBox = document.getElementById('submitResult');

      function showResult(correct, message) {
        resultBox.hidden = false;
        resultBox.className = 'submit-result ' + (correct ? 'result-correct' : 'result-wrong');
        resultBox.innerHTML = '<div class="result-icon">' + (correct ? '✓' : '✗') + '</div>' +
          '<div class="result-text">' + escapeHtml(message) + '</div>';
      }

      submitBtn.addEventListener('click', function () {
        var code = editor.value;
        var original = submitBtn.textContent;
        submitBtn.disabled = true;
        submitBtn.textContent = '提交中…';
        resultBox.hidden = true;
        Api.submitExercise(id, code).then(function (res) {
          submitBtn.disabled = false;
          submitBtn.textContent = original;
          var correct = !!res.correct;
          showResult(correct, res.message || (correct ? '答对了！' : '再想想，检查一下代码。'));
          if (correct) {
            return Api.markExercise(id, true).then(function () {
              toast('已记录练习进度', 'success');
            });
          }
        }).catch(function (err) {
          submitBtn.disabled = false;
          submitBtn.textContent = original;
          showResult(false, Api.friendlyMessage(err));
        });
      });

      resetBtn.addEventListener('click', function () {
        editor.value = starter;
        resultBox.hidden = true;
        editor.focus();
        toast('代码已重置');
      });
    }).catch(function (err) {
      if (isCurrent(token)) setError(Api.friendlyMessage(err), function () { viewExerciseDetail(id); });
    });
  }

  /* ==================== 视图 5：学习进度 ==================== */

  function progressList(title, ids, map, type) {
    var body;
    if (!Array.isArray(ids) || !ids.length) {
      body = '<p class="muted">还没有完成的项目，加油！</p>';
    } else {
      body = '<ul class="progress-items">' + ids.map(function (id) {
        var label = map[id] || ((type === 'lessons' ? '教程 #' : '练习 #') + id);
        return '<li><a href="#/' + type + '/' + encodeURIComponent(id) + '">' +
          '<span class="check">✓</span>' + escapeHtml(label) + '</a></li>';
      }).join('') + '</ul>';
    }
    return '<section class="panel"><h2 class="section-title">' + escapeHtml(title) + '</h2>' +
      body + '</section>';
  }

  function statCard(label, value, total) {
    return '<div class="stat-card"><div class="stat-value">' + escapeHtml(value) +
      ' <small>/ ' + escapeHtml(total) + '</small></div>' +
      '<div class="stat-label">' + escapeHtml(label) + '</div></div>';
  }

  function viewProgress() {
    var token = currentToken;
    setLoading();
    Promise.all([Api.getProgress(), Api.getLessons(), Api.getExercises()]).then(function (results) {
      if (!isCurrent(token)) return;
      var p = results[0] || {};
      var lessons = results[1] || [];
      var exercises = results[2] || [];
      var lessonMap = {}, exerciseMap = {};
      lessons.forEach(function (l) { lessonMap[l.id] = l.title; });
      exercises.forEach(function (e) { exerciseMap[e.id] = e.title; });

      var completedLessons = p.completed_lesson_ids || [];
      var completedExercises = p.completed_exercise_ids || [];
      var totalLessons = Number(p.total_lessons) || lessons.length;
      var totalExercises = Number(p.total_exercises) || exercises.length;
      var percent = Math.max(0, Math.min(100, Number(p.completion_percent) || 0));
      var lessonWidth = percentOf(completedLessons.length, totalLessons);
      var exerciseWidth = percentOf(completedExercises.length, totalExercises);

      app.innerHTML = '<div class="page">' +
        pageHeader('学习进度', '坚持学习，每一点进步都算数') +
        '<div class="progress-overview">' +
          '<div class="progress-ring" style="--percent:' + percent + '">' +
            '<div class="progress-ring-inner">' +
              '<span class="progress-ring-value">' + percent + '%</span>' +
              '<span class="progress-ring-label">总完成度</span>' +
            '</div>' +
          '</div>' +
          '<div class="progress-stats">' +
            statCard('已完成教程', completedLessons.length, totalLessons) +
            statCard('已完成练习', completedExercises.length, totalExercises) +
            '<div class="progress-bar-wrap">' +
              '<div class="progress-bar-label"><span>教程进度</span><span>' +
                completedLessons.length + ' / ' + totalLessons + '</span></div>' +
              '<div class="progress-bar"><div class="progress-bar-fill" data-width="' +
                lessonWidth + '%"></div></div>' +
              '<div class="progress-bar-label"><span>练习进度</span><span>' +
                completedExercises.length + ' / ' + totalExercises + '</span></div>' +
              '<div class="progress-bar"><div class="progress-bar-fill progress-bar-fill-alt" data-width="' +
                exerciseWidth + '%"></div></div>' +
            '</div>' +
          '</div>' +
        '</div>' +
        '<div class="progress-lists">' +
          progressList('已完成的教程', completedLessons, lessonMap, 'lessons') +
          progressList('已完成的练习', completedExercises, exerciseMap, 'exercises') +
        '</div>' +
      '</div>';

      // 下一帧再设置宽度，触发进度条过渡动画
      global.requestAnimationFrame(function () {
        if (!isCurrent(token)) return;
        var fills = app.querySelectorAll('.progress-bar-fill');
        Array.prototype.forEach.call(fills, function (fill) {
          fill.style.width = fill.getAttribute('data-width');
        });
      });
    }).catch(function (err) {
      if (isCurrent(token)) setError(Api.friendlyMessage(err), viewProgress);
    });
  }

  /* ==================== 路由 ==================== */

  function parseRoute() {
    return (global.location.hash || '').replace(/^#\/?/, '').split('/').filter(Boolean);
  }

  function updateNav() {
    var parts = parseRoute();
    var current = parts[0] || 'lessons';
    var links = document.querySelectorAll('#nav a');
    Array.prototype.forEach.call(links, function (link) {
      if (link.getAttribute('data-route') === current) link.classList.add('active');
      else link.classList.remove('active');
    });
  }

  function renderRoute() {
    currentToken += 1;
    updateNav();
    global.scrollTo(0, 0);

    var parts = parseRoute();
    if (!parts.length) {
      global.location.replace('#/lessons');
      return;
    }

    switch (parts[0]) {
      case 'lessons':
        if (parts[1]) viewLessonDetail(parts[1]);
        else viewLessons();
        break;
      case 'exercises':
        if (parts[1]) viewExerciseDetail(parts[1]);
        else viewExercises();
        break;
      case 'progress':
        viewProgress();
        break;
      default:
        app.innerHTML = '<div class="page"><div class="state state-error">' +
          '<div class="state-icon">?</div><h2>页面不存在</h2>' +
          '<p>没有找到这个页面，请从上方导航重新选择。</p>' +
          '<a class="btn btn-primary" href="#/lessons">返回教程</a>' +
          '</div></div>';
    }
  }

  function init() {
    app = document.getElementById('app');
    global.addEventListener('hashchange', renderRoute);
    renderRoute();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})(window);
