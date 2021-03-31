import Vue from "vue";
import Vuex, { StoreOptions } from "vuex";

import { mainModule } from "./main";
import { State } from "./state";

const storeOptions: StoreOptions<State> = {
  modules: {
    main: mainModule,
  },
};

export const store = new Vuex.Store<State>(storeOptions);

