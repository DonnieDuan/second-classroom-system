import http from '@ohos.net.http';

export const BASE_URL = 'http://localhost:8080/second-class/api';

export interface HttpRequestOptions {
  url: string;
  method: http.RequestMethod;
  extraData?: Object;
}

export interface ApiResult<T> {
  code: number;
  msg: string;
  data: T;
}

class HttpClient {
  async get<T>(url: string, params?: Record<string, string>): Promise<T> {
    let requestUrl: string = `${BASE_URL}${url}`;
    if (params) {
      let query: string = '';
      let keys: string[] = Object.keys(params);
      for (let i: number = 0; i < keys.length; i++) {
        let key: string = keys[i];
        if (i > 0) {
          query += '&';
        }
        query += encodeURIComponent(key) + '=' + encodeURIComponent(params[key]);
      }
      if (query.length > 0) {
        requestUrl += '?' + query;
      }
    }
    return await this.request<T>({ url: requestUrl, method: http.RequestMethod.GET });
  }

  async post<T>(url: string, data?: Object): Promise<T> {
    return await this.request<T>({
      url: `${BASE_URL}${url}`,
      method: http.RequestMethod.POST,
      extraData: data
    });
  }

  async request<T>(options: HttpRequestOptions): Promise<T> {
    return new Promise<T>((resolve: (value: T) => void, reject: (reason: Error) => void) => {
      // 每次请求创建新的 HttpRequest 实例，避免请求干扰
      let httpRequest: http.HttpRequest = http.createHttp();
      httpRequest.request(options.url, {
        method: options.method,
        header: {
          'Content-Type': 'application/json;charset=utf-8'
        },
        extraData: options.extraData,
        connectTimeout: 10000,
        readTimeout: 10000
      }, (err: Error, data: http.HttpResponse) => {
        if (err) {
          console.error(`HTTP请求失败: ${err.message}`);
          reject(err);
          httpRequest.destroy();
          return;
        }
        try {
          let resultStr: string;
          if (typeof data.result === 'string') {
            resultStr = data.result;
          } else {
            resultStr = JSON.stringify(data.result);
          }
          const result: T = JSON.parse(resultStr) as T;
          resolve(result);
        } catch (e) {
          console.error(`JSON解析失败: ${(e as Object).toString()}, 原始数据: ${data.result}`);
          reject(e as Error);
        } finally {
          httpRequest.destroy();
        }
      });
    });
  }
}

export const httpClient = new HttpClient();
