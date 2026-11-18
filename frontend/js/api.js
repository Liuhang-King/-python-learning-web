/**
 * api.js —— 类型化 fetch 封装
 * 严格遵循 CONTRACT.md 的 API 契约。
 * Base URL 从 window.API_BASE_URL 读取，默认 ''（同源）。
 */
(function (global) {
  'use strict';

  // 不硬编码绝对地址；留空表示同源（例如由后端在 5000 端口托管前端）
  var baseUrl = global.API_BASE_URL || '';

  // 后端 error.code -> 中文友好文案
  var ERROR_CODE_MESSAGES = {
    BAD_REQUEST: '请求有误',
    NOT_FOUND: '内容不存在',
    VALIDATION_ERROR: '填写有误',
    INTERNAL_ERROR: '服务暂时不可用'
  };

  var NETWORK_MESSAGE = '网络异常，请检查服务是否启动';
  var MAX_RETRIES = 3; // 仅 5xx 重试，最多 3 次

  function ApiError(status, code, serverMessage) {
    this.name = 'ApiError';
    this.status = status;
    this.code = code;
    this.serverMessage = serverMessage || '';
    this.friendlyMessage = ERROR_CODE_MESSAGES[code] ||
      this.serverMessage || '请求失败，请稍后重试';
    this.message = this.friendlyMessage;
  }
  ApiError.prototype = Object.create(Error.prototype);
  ApiError.prototype.constructor = ApiError;

  function NetworkError() {
    this.name = 'NetworkError';
    this.code = 'NETWORK_ERROR';
    this.friendlyMessage = NETWORK_MESSAGE;
    this.message = NETWORK_MESSAGE;
  }
  NetworkError.prototype = Object.create(Error.prototype);
  NetworkError.prototype.constructor = NetworkError;

  function sleep(ms) {
    return new Promise(function (resolve) { setTimeout(resolve, ms); });
  }

  /** 从任意错误对象中取出可展示的中文文案 */
  function friendlyMessage(error) {
    if (!error) return '未知错误';
    if (error.friendlyMessage) return error.friendlyMessage;
    if (typeof error === 'string') return error;
    return error.message || '未知错误';
  }

  /**
   * 统一请求：解析 JSON、映射错误码、5xx 指数退避重试、网络异常兜底。
   * @param {string} method HTTP 方法
   * @param {string} path 以 '/' 开头的 API 路径
   * @param {object|null} body JSON 请求体（自动设置 Content-Type）
   */
  function request(method, path, body) {
    var url = baseUrl + path;
    var attempt = 0;

    function doFetch() {
      var options = {
        method: method,
        headers: { 'Accept': 'application/json' }
      };
      if (body !== undefined && body !== null) {
        options.headers['Content-Type'] = 'application/json';
        options.body = JSON.stringify(body);
      }

      return fetch(url, options).then(function (response) {
        return response.text().then(function (text) {
          var data = null;
          if (text) {
            try { data = JSON.parse(text); } catch (e) { data = null; }
          }

          if (response.ok) return data;

          var code = (data && data.error && data.error.code) || 'INTERNAL_ERROR';
          var serverMessage = (data && data.error && data.error.message) || '';
          var err = new ApiError(response.status, code, serverMessage);

          // 4xx：不重试，直接抛出；5xx：指数退避重试（500/1000/2000ms）
          if (response.status >= 500 && attempt < MAX_RETRIES) {
            attempt += 1;
            return sleep(500 * Math.pow(2, attempt - 1)).then(doFetch);
          }
          throw err;
        });
      });
    }

    return doFetch().catch(function (error) {
      // 已封装的业务/网络错误原样透出；fetch 本身失败 -> 网络异常文案
      if (error instanceof ApiError || error instanceof NetworkError) throw error;
      throw new NetworkError();
    });
  }

  var api = {
    ApiError: ApiError,
    NetworkError: NetworkError,
    friendlyMessage: friendlyMessage,
    setBaseUrl: function (url) { baseUrl = url || ''; },
    getBaseUrl: function () { return baseUrl; },

    // 健康检查
    health: function () { return request('GET', '/api/health'); },
    ready: function () { return request('GET', '/api/ready'); },

    // 教程
    getLessons: function () { return request('GET', '/api/lessons'); },
    getLesson: function (id) {
      return request('GET', '/api/lessons/' + encodeURIComponent(id));
    },

    // 练习题
    getExercises: function () { return request('GET', '/api/exercises'); },
    getExercise: function (id) {
      return request('GET', '/api/exercises/' + encodeURIComponent(id));
    },
    submitExercise: function (id, code) {
      return request('POST', '/api/exercises/' + encodeURIComponent(id) + '/submit',
        { code: code });
    },

    // 学习进度
    getProgress: function () { return request('GET', '/api/progress'); },
    markLesson: function (id) {
      return request('POST', '/api/progress/lessons/' + encodeURIComponent(id), {});
    },
    markExercise: function (id, correct) {
      return request('POST', '/api/progress/exercises/' + encodeURIComponent(id), {
        correct: correct !== false
      });
    },

    // 系统自检
    selftest: function () { return request('GET', '/api/selftest'); }
  };

  global.Api = api;
})(window);
