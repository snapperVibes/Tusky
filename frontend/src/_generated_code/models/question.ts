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
/**
 * 
 * @export
 * @interface Question
 */
export interface Question {
    /**
     * 
     * @type {string}
     * @memberof Question
     */
    previousQuestion?: any;
    /**
     * 
     * @type {string}
     * @memberof Question
     */
    id?: any;
    /**
     * 
     * @type {string}
     * @memberof Question
     */
    query: any;
    /**
     * 
     * @type {string}
     * @memberof Question
     */
    quizId: any;
    /**
     * 
     * @type {Array&lt;Answer&gt;}
     * @memberof Question
     */
    answers: any;
}
