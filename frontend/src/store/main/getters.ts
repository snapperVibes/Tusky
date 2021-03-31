// @ts-ignore
import { getStoreAccessors} from "typesafe-vuex";
import { MainState } from "./state";
import { State } from "../state";

export const getters = {
  isLoggedIn: (state: MainState) => state.isLoggedIn,
};

const {read} = getStoreAccessors<MainState, State>("");

export const readIsLoggedIn = read(getters.isLoggedIn);


