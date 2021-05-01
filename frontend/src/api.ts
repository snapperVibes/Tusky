import {LoginApi, QuizzesApi, RoomsApi, UsersApi} from "@/_generated_code";
import * as _schema from "@/_generated_code/models"

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

  const [msg, malformed] = function () {
    let message: string | undefined
    try {
      message = err.response.data.detail;
    }
    catch (err){
      console.log("Something unexpected went wrong", err)
      return [message, true]
    }
    if (message === undefined) {
      console.log("Message detail was undefined")
      return [message, true]
    }
    if (message.includes("[object Object]")) {
      console.log("The message contained JavaScript", message)
      return [message, true]
    }
    return [message, false]
  }()

  if (malformed) {
    // Todo: Set up an API Endpoint to log this happens
    alert("Something went wrong.")
    return
  }
  alert(msg)
}

export const roomsApi = new RoomsApi()
export const usersApi = new UsersApi()
export const loginApi = new LoginApi()
export const quizzesApi = new QuizzesApi()
// Todo: I know this isn't export correctly
export const schema = _schema
