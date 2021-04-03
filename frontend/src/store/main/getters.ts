import { MainState } from '@/store/main/state'
import { getStoreAccessors } from 'typesafe-vuex'
import { State } from '../state'

export const getters = {
  loginError: (state: MainState) => state.logInError
}

const { read } = getStoreAccessors<MainState, State>('')

export const readLoginError = read(getters.loginError)
