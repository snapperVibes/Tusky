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
  async getUser(name: string, number: any) {
    return axios.get(`${apiUrl}/users/get-by-name`, {
      params: {
        name: name,
        number: number
      },
    });
  },

  async getQuiz(name: string, owner_id: string) {
    return axios.get(`${apiUrl}/quizzes/get`, {
      params: {
        name: name,
        owner_id: owner_id,
      },
    });
  },

  async modifyQuiz(id: string, name: string, owner_id: string) {
    return axios.put(`${apiUrl}/quizzes/update`, {
      id: id,
      name: name,
      owner_id: owner_id
    });

  }
};

export * from "./_generated_code/api"
// export * from "./configuration";
