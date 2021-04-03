import { api } from '@/api'
import { getStoreAccessors } from 'typesafe-vuex'
import { ActionContext } from 'vuex'
import { State } from '../state'
import { AppNotification, MainState } from './state'

type MainContext = ActionContext<MainState, State>;

export const actions = {
  async actionLogIn (context: MainContext, payload: { username: string; password: string}) {
    const response = await api.logInGetToken(payload.username, payload.password)
  }

}

const { dispatch } = getStoreAccessors<MainState | any, State>('')

export const dispatchLogIn = dispatch(actions.actionLogIn)
