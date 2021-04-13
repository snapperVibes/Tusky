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
import { UserCreate } from '../models';
import { UserPublic } from '../models';
/**
 * UsersApi - axios parameter creator
 * @export
 */
export const UsersApiAxiosParamCreator = function (configuration?: Configuration) {
    return {
        /**
         * 
         * @summary Create User
         * @param {UserCreate} body 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        createUserApiV1UsersCreatePost: async (body: UserCreate, options: any = {}): Promise<RequestArgs> => {
            // verify required parameter 'body' is not null or undefined
            if (body === null || body === undefined) {
                throw new RequiredError('body','Required parameter body was null or undefined when calling createUserApiV1UsersCreatePost.');
            }
            const localVarPath = `/api/v1/users/create`;
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
         * @summary Get By Name
         * @param {string} name 
         * @param {number} number 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        getByNameApiV1UsersGetByNameGet: async (name: string, number: number, options: any = {}): Promise<RequestArgs> => {
            // verify required parameter 'name' is not null or undefined
            if (name === null || name === undefined) {
                throw new RequiredError('name','Required parameter name was null or undefined when calling getByNameApiV1UsersGetByNameGet.');
            }
            // verify required parameter 'number' is not null or undefined
            if (number === null || number === undefined) {
                throw new RequiredError('number','Required parameter number was null or undefined when calling getByNameApiV1UsersGetByNameGet.');
            }
            const localVarPath = `/api/v1/users/get-by-name`;
            // use dummy base URL string because the URL constructor only accepts absolute URLs.
            const localVarUrlObj = new URL(localVarPath, 'https://example.com');
            let baseOptions;
            if (configuration) {
                baseOptions = configuration.baseOptions;
            }
            const localVarRequestOptions = { method: 'GET', ...baseOptions, ...options};
            const localVarHeaderParameter = {} as any;
            const localVarQueryParameter = {} as any;

            if (name !== undefined) {
                localVarQueryParameter['name'] = name;
            }

            if (number !== undefined) {
                localVarQueryParameter['number'] = number;
            }

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

            return {
                url: localVarUrlObj.pathname + localVarUrlObj.search + localVarUrlObj.hash,
                options: localVarRequestOptions,
            };
        },
        /**
         * 
         * @summary Read Current User
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        readCurrentUserApiV1UsersMeGet: async (options: any = {}): Promise<RequestArgs> => {
            const localVarPath = `/api/v1/users/me`;
            // use dummy base URL string because the URL constructor only accepts absolute URLs.
            const localVarUrlObj = new URL(localVarPath, 'https://example.com');
            let baseOptions;
            if (configuration) {
                baseOptions = configuration.baseOptions;
            }
            const localVarRequestOptions = { method: 'GET', ...baseOptions, ...options};
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

            return {
                url: localVarUrlObj.pathname + localVarUrlObj.search + localVarUrlObj.hash,
                options: localVarRequestOptions,
            };
        },
    }
};

/**
 * UsersApi - functional programming interface
 * @export
 */
export const UsersApiFp = function(configuration?: Configuration) {
    return {
        /**
         * 
         * @summary Create User
         * @param {UserCreate} body 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async createUserApiV1UsersCreatePost(body: UserCreate, options?: any): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<UserPublic>> {
            const localVarAxiosArgs = await UsersApiAxiosParamCreator(configuration).createUserApiV1UsersCreatePost(body, options);
            return (axios: AxiosInstance = globalAxios, basePath: string = BASE_PATH) => {
                const axiosRequestArgs = {...localVarAxiosArgs.options, url: basePath + localVarAxiosArgs.url};
                return axios.request(axiosRequestArgs);
            };
        },
        /**
         * 
         * @summary Get By Name
         * @param {string} name 
         * @param {number} number 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async getByNameApiV1UsersGetByNameGet(name: string, number: number, options?: any): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<UserPublic>> {
            const localVarAxiosArgs = await UsersApiAxiosParamCreator(configuration).getByNameApiV1UsersGetByNameGet(name, number, options);
            return (axios: AxiosInstance = globalAxios, basePath: string = BASE_PATH) => {
                const axiosRequestArgs = {...localVarAxiosArgs.options, url: basePath + localVarAxiosArgs.url};
                return axios.request(axiosRequestArgs);
            };
        },
        /**
         * 
         * @summary Read Current User
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async readCurrentUserApiV1UsersMeGet(options?: any): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<UserPublic>> {
            const localVarAxiosArgs = await UsersApiAxiosParamCreator(configuration).readCurrentUserApiV1UsersMeGet(options);
            return (axios: AxiosInstance = globalAxios, basePath: string = BASE_PATH) => {
                const axiosRequestArgs = {...localVarAxiosArgs.options, url: basePath + localVarAxiosArgs.url};
                return axios.request(axiosRequestArgs);
            };
        },
    }
};

/**
 * UsersApi - factory interface
 * @export
 */
export const UsersApiFactory = function (configuration?: Configuration, basePath?: string, axios?: AxiosInstance) {
    return {
        /**
         * 
         * @summary Create User
         * @param {UserCreate} body 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        createUserApiV1UsersCreatePost(body: UserCreate, options?: any): AxiosPromise<UserPublic> {
            return UsersApiFp(configuration).createUserApiV1UsersCreatePost(body, options).then((request) => request(axios, basePath));
        },
        /**
         * 
         * @summary Get By Name
         * @param {string} name 
         * @param {number} number 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        getByNameApiV1UsersGetByNameGet(name: string, number: number, options?: any): AxiosPromise<UserPublic> {
            return UsersApiFp(configuration).getByNameApiV1UsersGetByNameGet(name, number, options).then((request) => request(axios, basePath));
        },
        /**
         * 
         * @summary Read Current User
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        readCurrentUserApiV1UsersMeGet(options?: any): AxiosPromise<UserPublic> {
            return UsersApiFp(configuration).readCurrentUserApiV1UsersMeGet(options).then((request) => request(axios, basePath));
        },
    };
};

/**
 * UsersApi - object-oriented interface
 * @export
 * @class UsersApi
 * @extends {BaseAPI}
 */
export class UsersApi extends BaseAPI {
    /**
     * 
     * @summary Create User
     * @param {UserCreate} body 
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof UsersApi
     */
    public createUserApiV1UsersCreatePost(body: UserCreate, options?: any) {
        return UsersApiFp(this.configuration).createUserApiV1UsersCreatePost(body, options).then((request) => request(this.axios, this.basePath));
    }
    /**
     * 
     * @summary Get By Name
     * @param {string} name 
     * @param {number} number 
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof UsersApi
     */
    public getByNameApiV1UsersGetByNameGet(name: string, number: number, options?: any) {
        return UsersApiFp(this.configuration).getByNameApiV1UsersGetByNameGet(name, number, options).then((request) => request(this.axios, this.basePath));
    }
    /**
     * 
     * @summary Read Current User
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof UsersApi
     */
    public readCurrentUserApiV1UsersMeGet(options?: any) {
        return UsersApiFp(this.configuration).readCurrentUserApiV1UsersMeGet(options).then((request) => request(this.axios, this.basePath));
    }
}
