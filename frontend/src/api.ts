import axios from "axios";

const apiUrl = "http://localhost:8000/api/v1";

function authHeaders(token: string) {
  return {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
}

export const api = {
  async getQuiz(owner: string, name: string) {
    return axios.get(`${apiUrl}/quizzes/get`, {
      params: {
        quiz_name: name,
        owner_name: owner,
      },
    });
  },
  async getQuestions(quiz_id: string) {
    return axios.get(`${apiUrl}/answers/get_by_quiz`, {
      params: {
        quiz_id: quiz_id,
      },
    });
  },
};
