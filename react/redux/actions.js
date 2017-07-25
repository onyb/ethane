import { getAccountInfo } from '../api';

export const SELECT_TOKEN = 'SELECT_TOKEN'
export const REFRESH_BALANCES = 'REFRESH_BALANCES'

export const selectToken = id => ({ type: SELECT_TOKEN, id })

export const updateBalances = () => async (dispatch) => {
    const response = await getAccountInfo();
    console.log(response)
    await dispatch({ type: REFRESH_BALANCES, payload: response.data });
}