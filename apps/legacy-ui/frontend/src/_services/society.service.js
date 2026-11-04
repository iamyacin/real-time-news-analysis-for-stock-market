import { Config } from '../config'
import { authHeader, handleResponse } from '../_helpers';

export const societyService = {
    getAll,
    getById,
    getNews,
    getOps,
    getOpsDate,
    getNewsWithoutPaging,
    getOpsLastMonths,
    getOpsPerMonth,
    getSectors,
    getBySector,
    topNews,
    getAllOpsDate
};

function getAll() {
    const requestOptions = { method: 'GET', headers: authHeader() };
    return fetch(`${Config.apiURL}/api/societies`, requestOptions)
      .then(handleResponse)
      .then(societies => {
        return societies
      });
}

function getById(id) {
  const requestOptions = { method: 'GET', headers: authHeader() };
  return fetch(`${Config.apiURL}/api/societies/${id}`, requestOptions)
    .then(handleResponse)
    .then(society => {
      return society
    });
}

function getBySector(sector) {
  const requestOptions = { method: 'GET', headers: authHeader() };
  return fetch(`${Config.apiURL}/api/societies-sector/${sector}`, requestOptions)
    .then(handleResponse)
    .then(societies => {
      return societies
    });
}

function getNews(symbol, page) {
  const requestOptions = { method: 'GET', headers: authHeader() };
  return fetch(`${Config.apiURL}/api/news/ticker/${symbol}/${page}/30`, requestOptions)
    .then(handleResponse)
    .then(news => {
      return news
    });
}

function topNews() {
  const requestOptions = { method: 'GET', headers: authHeader() };
  return fetch(`${Config.apiURL}/api/news/all-ops`, requestOptions)
    .then(handleResponse)
    .then(news => {
      return news
    });
}

function getNewsWithoutPaging(symbol) {
  const requestOptions = { method: 'GET', headers: authHeader() };
  return fetch(`${Config.apiURL}/api/news/ticker/${symbol}`, requestOptions)
    .then(handleResponse)
    .then(news => {
      return news
    });
}

function getOps(symbol) {
  const requestOptions = { method: 'GET', headers: authHeader() };
  return fetch(`${Config.apiURL}/api/news/ops/${symbol}`, requestOptions)
    .then(handleResponse)
    .then(ops => {
      return ops
    });
}

function getOpsLastMonths(symbol, days) {
  const requestOptions = { method: 'GET', headers: authHeader() };
  return fetch(`${Config.apiURL}/api/news/ops-last-month/${symbol}/${days}`, requestOptions)
    .then(handleResponse)
    .then(ops => {
      return ops
    });
}

function getOpsDate(symbol) {
  const requestOptions = { method: 'GET', headers: authHeader() };
  return fetch(`${Config.apiURL}/api/news/ops-date/${symbol}`, requestOptions)
    .then(handleResponse)
    .then(ops => {
      return ops
    });
}

function getAllOpsDate() {
  const requestOptions = { method: 'GET', headers: authHeader() };
  return fetch(`${Config.apiURL}/api/news/all-ops-date`, requestOptions)
    .then(handleResponse)
    .then(ops => {
      return ops
    });
}

function getOpsPerMonth(symbol) {
  const requestOptions = { method: 'GET', headers: authHeader() };
  return fetch(`${Config.apiURL}/api/news/ops-month/${symbol}`, requestOptions)
    .then(handleResponse)
    .then(ops => {
      return ops
    });
}

function getSectors() {
    const requestOptions = { method: 'GET', headers: authHeader() };
    return fetch(`${Config.apiURL}/api/sectors`, requestOptions)
      .then(handleResponse)
      .then(sectors => {
        return sectors
      });
}
