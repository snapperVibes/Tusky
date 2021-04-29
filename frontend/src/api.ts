import {LoginApi, RoomsApi, UsersApi} from "@/_generated_code";

// TODO: COMPLETE OVERHAUL OF API SYSTEM
// The generated code doesn't work how I envisioned.
// For example
// {displayName: "asdf"} should work; the types support this.
// However, the code passes the literal "displayName" to the server instead of changing
// it back to "display_name"


export function authHeaders(token: string) {
  return {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
}

export function displayError(err: any) {
  // Raises an "alert" with the error detailed by the api.
  // Malformed errors just say "Something went wrong".
  const malformedMessage = function () {
    const message = err.response.data.detail;
    if (message === undefined) {
      return true
    }
    if (message == "[object Object]") {
      return true
    }
    alert(err.response.data.detail)
  }()
  if (malformedMessage) {
    // Todo: Set up an API Endpoint to log this happens
    alert("Something went wrong")
  }
}

export const roomsApi = new RoomsApi()
export const usersApi = new UsersApi()
export const loginApi = new LoginApi()
