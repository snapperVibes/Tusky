/* tslint:disable */
/* eslint-disable */
/**
 * FastAPI
 * No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)
 *
 * OpenAPI spec version: 0.1.0
 * 
 *
 * NOTE: This class is auto generated by the swagger code generator program.
 * https://github.com/swagger-api/swagger-codegen.git
 * Do not edit the class manually.
 */
import globalAxios, { AxiosPromise, AxiosInstance } from 'axios';
import { Configuration } from '../configuration';
// Some imports not used depending on template conditions
// @ts-ignore
import { BASE_PATH, COLLECTION_FORMATS, RequestArgs, BaseAPI, RequiredError } from '../base';
import { HTTPValidationError } from '../models';
import { QuizSession } from '../models';
import { QuizSessionCreate } from '../models';
import { QuizSessionUpdate } from '../models';
import { StudentResponse } from '../models';
import { StudentResponseCreate } from '../models';
/**
 * SessionsApi - axios parameter creator
 * @export
 */
export const SessionsApiAxiosParamCreator = function (configuration?: Configuration) {
    return {
        /**
         * 
         * @summary Create Session
         * @param {QuizSessionCreate} body 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        createSession: async (body: QuizSessionCreate, options: any = {}): Promise<RequestArgs> => {
            // verify required parameter 'body' is not null or undefined
            if (body === null || body === undefined) {
                throw new RequiredError('body','Required parameter body was null or undefined when calling createSession.');
            }
            const localVarPath = `/api/v1/sessions/create`;
            // use dummy base URL string because the URL constructor only accepts absolute URLs.
            const localVarUrlObj = new URL(localVarPath, 'https://example.com');
            let baseOptions;
            if (configuration) {
                baseOptions = configuration.baseOptions;
            }
            const localVarRequestOptions = { method: 'POST', ...baseOptions, ...options};
            const localVarHeaderParameter = {} as any;
            const localVarQueryParameter = {} as any;

            // authentication OAuth2PasswordBearer required
            // oauth required
            if (configuration && configuration.accessToken) {
                const localVarAccessTokenValue = typeof configuration.accessToken === 'function'
                    ? await configuration.accessToken("OAuth2PasswordBearer", [])
                    : await configuration.accessToken;
                localVarHeaderParameter["Authorization"] = "Bearer " + localVarAccessTokenValue;
            }

            localVarHeaderParameter['Content-Type'] = 'application/json';

            const query = new URLSearchParams(localVarUrlObj.search);
            for (const key in localVarQueryParameter) {
                query.set(key, localVarQueryParameter[key]);
            }
            for (const key in options.query) {
                query.set(key, options.query[key]);
            }
            localVarUrlObj.search = (new URLSearchParams(query)).toString();
            let headersFromBaseOptions = baseOptions && baseOptions.headers ? baseOptions.headers : {};
            localVarRequestOptions.headers = {...localVarHeaderParameter, ...headersFromBaseOptions, ...options.headers};
            const needsSerialization = (typeof body !== "string") || localVarRequestOptions.headers['Content-Type'] === 'application/json';
            localVarRequestOptions.data =  needsSerialization ? JSON.stringify(body !== undefined ? body : {}) : (body || "");

            return {
                url: localVarUrlObj.pathname + localVarUrlObj.search + localVarUrlObj.hash,
                options: localVarRequestOptions,
            };
        },
        /**
         * 
         * @summary Create Student Response
         * @param {StudentResponseCreate} body 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        createStudentResponse: async (body: StudentResponseCreate, options: any = {}): Promise<RequestArgs> => {
            // verify required parameter 'body' is not null or undefined
            if (body === null || body === undefined) {
                throw new RequiredError('body','Required parameter body was null or undefined when calling createStudentResponse.');
            }
            const localVarPath = `/api/v1/sessions/response/create`;
            // use dummy base URL string because the URL constructor only accepts absolute URLs.
            const localVarUrlObj = new URL(localVarPath, 'https://example.com');
            let baseOptions;
            if (configuration) {
                baseOptions = configuration.baseOptions;
            }
            const localVarRequestOptions = { method: 'POST', ...baseOptions, ...options};
            const localVarHeaderParameter = {} as any;
            const localVarQueryParameter = {} as any;

            // authentication OAuth2PasswordBearer required
            // oauth required
            if (configuration && configuration.accessToken) {
                const localVarAccessTokenValue = typeof configuration.accessToken === 'function'
                    ? await configuration.accessToken("OAuth2PasswordBearer", [])
                    : await configuration.accessToken;
                localVarHeaderParameter["Authorization"] = "Bearer " + localVarAccessTokenValue;
            }

            localVarHeaderParameter['Content-Type'] = 'application/json';

            const query = new URLSearchParams(localVarUrlObj.search);
            for (const key in localVarQueryParameter) {
                query.set(key, localVarQueryParameter[key]);
            }
            for (const key in options.query) {
                query.set(key, options.query[key]);
            }
            localVarUrlObj.search = (new URLSearchParams(query)).toString();
            let headersFromBaseOptions = baseOptions && baseOptions.headers ? baseOptions.headers : {};
            localVarRequestOptions.headers = {...localVarHeaderParameter, ...headersFromBaseOptions, ...options.headers};
            const needsSerialization = (typeof body !== "string") || localVarRequestOptions.headers['Content-Type'] === 'application/json';
            localVarRequestOptions.data =  needsSerialization ? JSON.stringify(body !== undefined ? body : {}) : (body || "");

            return {
                url: localVarUrlObj.pathname + localVarUrlObj.search + localVarUrlObj.hash,
                options: localVarRequestOptions,
            };
        },
        /**
         * 
         * @summary Update Session
         * @param {QuizSessionUpdate} body 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        updateSession: async (body: QuizSessionUpdate, options: any = {}): Promise<RequestArgs> => {
            // verify required parameter 'body' is not null or undefined
            if (body === null || body === undefined) {
                throw new RequiredError('body','Required parameter body was null or undefined when calling updateSession.');
            }
            const localVarPath = `/api/v1/sessions/update`;
            // use dummy base URL string because the URL constructor only accepts absolute URLs.
            const localVarUrlObj = new URL(localVarPath, 'https://example.com');
            let baseOptions;
            if (configuration) {
                baseOptions = configuration.baseOptions;
            }
            const localVarRequestOptions = { method: 'PATCH', ...baseOptions, ...options};
            const localVarHeaderParameter = {} as any;
            const localVarQueryParameter = {} as any;

            // authentication OAuth2PasswordBearer required
            // oauth required
            if (configuration && configuration.accessToken) {
                const localVarAccessTokenValue = typeof configuration.accessToken === 'function'
                    ? await configuration.accessToken("OAuth2PasswordBearer", [])
                    : await configuration.accessToken;
                localVarHeaderParameter["Authorization"] = "Bearer " + localVarAccessTokenValue;
            }

            localVarHeaderParameter['Content-Type'] = 'application/json';

            const query = new URLSearchParams(localVarUrlObj.search);
            for (const key in localVarQueryParameter) {
                query.set(key, localVarQueryParameter[key]);
            }
            for (const key in options.query) {
                query.set(key, options.query[key]);
            }
            localVarUrlObj.search = (new URLSearchParams(query)).toString();
            let headersFromBaseOptions = baseOptions && baseOptions.headers ? baseOptions.headers : {};
            localVarRequestOptions.headers = {...localVarHeaderParameter, ...headersFromBaseOptions, ...options.headers};
            const needsSerialization = (typeof body !== "string") || localVarRequestOptions.headers['Content-Type'] === 'application/json';
            localVarRequestOptions.data =  needsSerialization ? JSON.stringify(body !== undefined ? body : {}) : (body || "");

            return {
                url: localVarUrlObj.pathname + localVarUrlObj.search + localVarUrlObj.hash,
                options: localVarRequestOptions,
            };
        },
    }
};

/**
 * SessionsApi - functional programming interface
 * @export
 */
export const SessionsApiFp = function(configuration?: Configuration) {
    return {
        /**
         * 
         * @summary Create Session
         * @param {QuizSessionCreate} body 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async createSession(body: QuizSessionCreate, options?: any): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<QuizSession>> {
            const localVarAxiosArgs = await SessionsApiAxiosParamCreator(configuration).createSession(body, options);
            return (axios: AxiosInstance = globalAxios, basePath: string = BASE_PATH) => {
                const axiosRequestArgs = {...localVarAxiosArgs.options, url: basePath + localVarAxiosArgs.url};
                return axios.request(axiosRequestArgs);
            };
        },
        /**
         * 
         * @summary Create Student Response
         * @param {StudentResponseCreate} body 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async createStudentResponse(body: StudentResponseCreate, options?: any): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<StudentResponse>> {
            const localVarAxiosArgs = await SessionsApiAxiosParamCreator(configuration).createStudentResponse(body, options);
            return (axios: AxiosInstance = globalAxios, basePath: string = BASE_PATH) => {
                const axiosRequestArgs = {...localVarAxiosArgs.options, url: basePath + localVarAxiosArgs.url};
                return axios.request(axiosRequestArgs);
            };
        },
        /**
         * 
         * @summary Update Session
         * @param {QuizSessionUpdate} body 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async updateSession(body: QuizSessionUpdate, options?: any): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<QuizSession>> {
            const localVarAxiosArgs = await SessionsApiAxiosParamCreator(configuration).updateSession(body, options);
            return (axios: AxiosInstance = globalAxios, basePath: string = BASE_PATH) => {
                const axiosRequestArgs = {...localVarAxiosArgs.options, url: basePath + localVarAxiosArgs.url};
                return axios.request(axiosRequestArgs);
            };
        },
    }
};

/**
 * SessionsApi - factory interface
 * @export
 */
export const SessionsApiFactory = function (configuration?: Configuration, basePath?: string, axios?: AxiosInstance) {
    return {
        /**
         * 
         * @summary Create Session
         * @param {QuizSessionCreate} body 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        createSession(body: QuizSessionCreate, options?: any): AxiosPromise<QuizSession> {
            return SessionsApiFp(configuration).createSession(body, options).then((request) => request(axios, basePath));
        },
        /**
         * 
         * @summary Create Student Response
         * @param {StudentResponseCreate} body 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        createStudentResponse(body: StudentResponseCreate, options?: any): AxiosPromise<StudentResponse> {
            return SessionsApiFp(configuration).createStudentResponse(body, options).then((request) => request(axios, basePath));
        },
        /**
         * 
         * @summary Update Session
         * @param {QuizSessionUpdate} body 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        updateSession(body: QuizSessionUpdate, options?: any): AxiosPromise<QuizSession> {
            return SessionsApiFp(configuration).updateSession(body, options).then((request) => request(axios, basePath));
        },
    };
};

/**
 * SessionsApi - object-oriented interface
 * @export
 * @class SessionsApi
 * @extends {BaseAPI}
 */
export class SessionsApi extends BaseAPI {
    /**
     * 
     * @summary Create Session
     * @param {QuizSessionCreate} body 
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof SessionsApi
     */
    public createSession(body: QuizSessionCreate, options?: any) {
        return SessionsApiFp(this.configuration).createSession(body, options).then((request) => request(this.axios, this.basePath));
    }
    /**
     * 
     * @summary Create Student Response
     * @param {StudentResponseCreate} body 
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof SessionsApi
     */
    public createStudentResponse(body: StudentResponseCreate, options?: any) {
        return SessionsApiFp(this.configuration).createStudentResponse(body, options).then((request) => request(this.axios, this.basePath));
    }
    /**
     * 
     * @summary Update Session
     * @param {QuizSessionUpdate} body 
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof SessionsApi
     */
    public updateSession(body: QuizSessionUpdate, options?: any) {
        return SessionsApiFp(this.configuration).updateSession(body, options).then((request) => request(this.axios, this.basePath));
    }
}
