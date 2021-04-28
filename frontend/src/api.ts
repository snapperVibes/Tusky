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
  const message = err.response.data.detail;
  if (message !== undefined){
    alert(err.response.data.detail)
  }
  // Todo: Set up an API Endpoint to log this happens
  alert("Something went wrong.")
}

// export * from "@/_generated_code/api";


// export * from "./configuration";

export const roomsApi = new RoomsApi()
export const usersApi = new UsersApi()
export const loginApi = new LoginApi()
