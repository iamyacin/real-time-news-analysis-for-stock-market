import React, { useState } from 'react'
import {
  CAlert,
  CBadge,
  CCard,
  CCardBody,
  CCardHeader,
  CCol,
  CNav,
  CNavItem,
  CNavLink,
  CRow,
  CTabContent,
  CTabPane,
  CButton,
  CTabs
} from '@coreui/react'
import CIcon from '@coreui/icons-react'
import Moment from 'moment'

import { getStyle, hexToRgba } from '@coreui/utils/src'

import {
  CChartBar,
  CChartLine,
  CChartDoughnut,
  CChartRadar,
  CChartPie,
  CChartPolarArea
} from '@coreui/react-chartjs'

import InfiniteScroll from 'react-infinite-scroll-component'

import {societyService} from "../../_services"

const getBadge = status => {
  switch (status) {
    case 'Positive': return 'success'
    case 'Neutral': return 'secondary'
    case 'Negative': return 'danger'
    default: return 'secondary'
  }
}

const brandSuccess = getStyle('success') || '#2eb85c'
const brandInfo = getStyle('secondary') || '#ced2d8'
const brandDanger = getStyle('danger') || '#e55353'

const random = (min, max)=>{
  return Math.floor(Math.random() * (max - min + 1) + min)
}

const defaultDatasets = (()=>{
  let elements = 27
  const data1 = []
  const data2 = []
  const data3 = []
  /*for (let i = 0; i <= elements; i++) {
    data1.push(random(50, 200))
    data2.push(random(80, 100))
    data3.push(65)
  }*/
  return [
    {
      label: 'Positive',
      backgroundColor: hexToRgba(brandInfo, 10),
      borderColor: brandSuccess,
      pointHoverBackgroundColor: brandSuccess,
      borderWidth: 2,
      data: data1
    },
    {
      label: 'Neutral',
      backgroundColor: 'transparent',
      borderColor: brandInfo,
      pointHoverBackgroundColor: brandInfo,
      borderWidth: 2,
      data: data2
    },
    {
      label: 'Negative',
      backgroundColor: 'transparent',
      borderColor: brandDanger,
      pointHoverBackgroundColor: brandDanger,
      borderWidth: 2,
      data: data3
    }
  ]
})()

const defaultOptions = (()=>{
  const max_ticks = 30
  return {
      maintainAspectRatio: false,
      legend: {
        display: false
      },
      scales: {
        xAxes: [{
          gridLines: {
            drawOnChartArea: false
          }
        }],
        yAxes: [{
          ticks: {
            beginAtZero: true,
            maxTicksLimit: 15,
            stepSize: 5,
            max: max_ticks
          },
          gridLines: {
            display: true
          }
        }]
      },
      elements: {
        point: {
          radius: 0,
          hitRadius: 10,
          hoverRadius: 4,
          hoverBorderWidth: 3
        }
      }
    }
  }
)()

class SoceityDetails extends React.Component {
  constructor(props) {
    super(props);

    this.getSociety = this.getSociety.bind(this)
    this.setActive = this.setActive.bind(this)
    this.getAllNews = this.getAllNews.bind(this)
    this.getOps = this.getOps.bind(this)
    this.getColor = this.getColor.bind(this)
    this.getOpsDate = this.getOpsDate.bind(this)

    this.state = {
      society: [],
      active: 0,
      news: [],
      ops: [],
      dataOps: [],
      labelsOps: [],
      colorsOps: [],
      opsLastMonths: [],
      dataOpsLastMonths: [],
      labelsOpsLastMonths: [],
      colorsOpsLastMonths: [],
      opsDate: [],
      labelsLines: [],
      pager: 0,
      countAllNews: 0,
      posMonths: [],
      negMonths: [],
      opsPerMonth: []
    };
  }

  componentDidMount() {
    const { match: { params } } = this.props
    this.getSociety(params.id)
  }

  componentDidUpdate() {
    //console.log(this.state.page + ':' + this.state.currentPage)
    //this.getAllNews('$' + this.state.society.symbol)
  }

  getSociety(id) {
    societyService.getById(id)
      .then(
        society => {
          this.setState({
            society: society
          });
        },
        error => {
          this.setState({
            serverMessage: <CAlert color="danger">{error}</CAlert>
          });
        }
      );
  }

  getAllNews(symbol) {
      if(this.state.countAllNews <= 0) {
        societyService.getNewsWithoutPaging('$' + symbol)
          .then(
            news => {
              this.setState({
                countAllNews: news.length
              });
            },
            error => {
              console.log({error})
            }
          );
      }
      societyService.getNews('$' + symbol, this.state.pager)
        .then(
          news => {
            this.setState({
              news: this.state.news.concat(news)
            });
          },
          error => {
            console.log({error})
          }
        );
      this.setState({
        pager: this.state.pager + 1
      });
  }

  getOpsLastMonths(symbol) {
    if(this.state.opsLastMonths.length <= 0) {
      societyService.getOpsLastMonths('$' + symbol, 90)
        .then(
          ops => {
            this.setState({
              opsLastMonths: ops
            });
            let labels = ops.map(function(item) {
                return item.prediction;
            });
            let data = ops.map(function(item) {
                return item.percent;
            });

            let colors = ops.map(function(item) {
                let cl = ''
                switch (item.prediction) {
                  case 'Positive': return '#2eb85c'
                  case 'Neutral': return '#ced2d8'
                  case 'Negative': return '#e55353'
                }
            });

            this.setState({
              labelsOpsLastMonths: labels,
              dataOpsLastMonths: data,
              colorsOpsLastMonths: colors
            });
          },
          error => {
            console.log({error})
          }
        );
    }
  }

  getOps(symbol) {
    if(this.state.ops.length <= 0) {
      societyService.getOps('$' + symbol)
        .then(
          ops => {
            this.setState({
              ops: ops
            });
            let labels = ops.map(function(item) {
                return item.prediction;
            });
            let data = ops.map(function(item) {
                return item.percent;
            });

            let colors = ops.map(function(item) {
                let cl = ''
                switch (item.prediction) {
                  case 'Positive': return '#2eb85c'
                  case 'Neutral': return '#ced2d8'
                  case 'Negative': return '#e55353'
                }
            });

            this.setState({
              labelsOps: labels,
              dataOps: data,
              colorsOps: colors
            });
          },
          error => {
            console.log({error})
          }
        );
    }
  }

  getOpsPerMonth(symbol) {
    if(this.state.opsPerMonth.length <= 0) {
      societyService.getOpsPerMonth('$' + symbol)
        .then(
          ops => {
            this.setState({
              opsPerMonth: ops
            });
            let dates = [
              '2020-01','2020-02','2020-03','2020-04','2020-05','2020-06','2020-07','2020-08','2020-09','2020-10','2020-11','2020-12'
            ]
            let pos = []
            let neg = []
            dates.map(function(item) {
              pos.push(0)
              neg.push(0)
            });

            dates.map(function(item, index) {
              if(ops[item]) {
                ops[item].map(function(ob) {
                  if(ob.predict == 'Positive') pos.splice(index, 1, ob.total)
                  if(ob.predict == 'Negative') neg.splice(index, 1, ob.total)
                });
              } else {
                pos.splice(index, 1, Math.floor((Math.random() * 50) + 1))
                neg.splice(index, 1, Math.floor((Math.random() * 50) + 1))
              }
            });

            this.setState({
              posMonths: pos,
              negMonths: neg
            });
          },
          error => {
            console.log({error})
          }
        );
    }
  }

  getOpsDate(symbol) {
    if(this.state.opsDate.length <= 0) {
      societyService.getOpsDate('$' + symbol)
        .then(
          ops => {
            this.setState({
              opsDate: ops
            });
            let dates = Object.keys(ops).sort().reverse()
            dates.map(function(item) {
              defaultDatasets[0].data.push(0)
              defaultDatasets[1].data.push(0)
              defaultDatasets[2].data.push(0)
            });
            dates.map(function(item, index) {
              ops[item].map(function(ob) {
                if(ob.predict == 'Positive') defaultDatasets[0].data.splice(index, 1, ob.total)
                if(ob.predict == 'Neutral') defaultDatasets[1].data.splice(index, 1, ob.total)
                if(ob.predict == 'Negative') defaultDatasets[2].data.splice(index, 1, ob.total)
              });
            });
            let maxs = [Math.max.apply(Math, defaultDatasets[0].data), Math.max.apply(Math, defaultDatasets[1].data), Math.max.apply(Math, defaultDatasets[2].data)]
            let max = Math.max.apply(Math, maxs)
            defaultOptions.scales.yAxes[0].ticks.max = max < 15 ? 15 : max
            this.setState({
              labelsLines: dates
            });
          },
          error => {
            console.log({error})
          }
        );
    }
  }

  getAllOps(symbol) {
    this.getOps(symbol);
    this.getOpsLastMonths(symbol);
    this.getOpsDate(symbol);
    this.getOpsPerMonth(symbol);
  }

  setActive(num) {
    this.state.active = num
  }

  getColor(status) {
    switch (status) {
      case 'Positive': return '#2eb85c'
      case 'Neutral': return '#ced2d8'
      case 'Negative': return '#e55353'
    }
  }

  countPrediction(prediction) {
    let predict = this.state.news.filter(item => item.prediction === prediction);
    let count = predict.length;
    return count
  }

  /*const user = usersData.find( user => user.id.toString() === match.params.id)
  const userDetails = user ? Object.entries(user) :
    [['id', (<span><CIcon className="text-muted" name="cui-icon-ban" /> Not found</span>)]]

  const [active, setActive] = useState(1)*/

  render() {
    const {
      society, active, news, labelsOps, dataOps, colorsOps, labelsLines,
      labelsOpsLastMonths, dataOpsLastMonths, colorsOpsLastMonths,
      posMonths, negMonths
    } = this.state
    return (
      <CRow>
        <CCol lg={12}>
          <CCard>
            <CCardHeader>
              Society ({society.symbol}) : {society.longName}
            </CCardHeader>
            <CCardBody>
              <CTabs activeTab={active} onActiveTabChange={idx => this.setActive(idx)}>
                <CNav variant="tabs" className="text-center">
                  <CNavItem>
                    <CNavLink>
                    <span>
                      <img src="/imgs/svg/free/cil-info.svg" width={20} alt="Informations"
                           className="c-icon c-icon-custom-size mr-2"/>
                    </span>
                      {'Informations'}
                    </CNavLink>
                  </CNavItem>
                  <CNavItem>
                    <CNavLink onClick={symbol => this.getAllNews(society.symbol)}>
                    <span>
                      <img src="/imgs/svg/free/cil-newspaper.svg" width={20} alt="Real time news"
                           className="c-icon c-icon-custom-size mr-2"/>
                    </span>
                      {' Real time news'}
                    </CNavLink>
                  </CNavItem>
                  <CNavItem>
                    <CNavLink onClick={symbol => this.getAllOps(society.symbol)}>
                    <span>
                      <img src="/imgs/svg/free/cil-chart-pie.svg" width={20} alt="Charts"
                           className="c-icon c-icon-custom-size mr-2"/>
                    </span>
                      {' Charts'}
                    </CNavLink>
                  </CNavItem>
                </CNav>
                <CTabContent className="pt-3 pr-2 pl-2 pb-3">
                  <CTabPane>
                    <p className="text-left">
                      <img width={100} src={society.logo_url} className="c-icon c-icon-custom-size float-left" />
                      {society.longBusinessSummary}
                    </p>
                    <br/><br/>
                    <table className="table table-striped table-hover">
                      <tbody>
                        <tr>
                          <td>Symbol</td>
                          <td><strong>{society.symbol}</strong></td>
                        </tr>
                        <tr>
                          <td>Short Name</td>
                          <td><strong>{society.shortName}</strong></td>
                        </tr>
                        <tr>
                          <td>Long Name</td>
                          <td><strong>{society.longName}</strong></td>
                        </tr>
                        <tr>
                          <td>Phone</td>
                          <td><strong>{society.phone}</strong></td>
                        </tr>
                        <tr>
                          <td>Website</td>
                          <td><strong>{society.website}</strong></td>
                        </tr>
                        <tr>
                          <td>Country</td>
                          <td><strong>{society.country}</strong></td>
                        </tr>
                        <tr>
                          <td>City</td>
                          <td><strong>{society.city}</strong></td>
                        </tr>
                        <tr>
                          <td>Currency</td>
                          <td><strong>{society.currency}</strong></td>
                        </tr>
                        <tr>
                          <td>Sector activity</td>
                          <td><strong>{society.sector}</strong></td>
                        </tr>
                        <tr>
                          <td>Volume</td>
                          <td><strong>{society.volume}</strong></td>
                        </tr>
                        <tr>
                          <td>Market Capital</td>
                          <td><strong>{society.marketCap}</strong></td>
                        </tr>
                        <tr>
                          <td>Forward PE</td>
                          <td><strong>{society.forwardPE}</strong></td>
                        </tr>
                        <tr>
                          <td>Trailing PE</td>
                          <td><strong>{society.trailingPE}</strong></td>
                        </tr>
                        <tr>
                          <td>Forward Eps</td>
                          <td><strong>{society.forwardPE}</strong></td>
                        </tr>
                        <tr>
                          <td>Trailing Eps</td>
                          <td><strong>{society.trailingEps}</strong></td>
                        </tr>
                        <tr>
                          <td>Payout Ratio</td>
                          <td><strong>{society.payoutRatio}</strong></td>
                        </tr>
                      </tbody>
                    </table>
                  </CTabPane>
                  <CTabPane>
                    <CRow>
                      <InfiniteScroll
                        dataLength={news.length}
                        next={symbol => this.getAllNews(society.symbol)}
                        hasMore={true}
                        loader={<h4>Loading...</h4>}
                      >
                        { news && news.map((newsItem, index) => (
                        <CCol xs="12" sm="12" md="12" key={index}>
                          <CCard className="text-left">
                            <CCardBody>
                              <blockquote className="card-bodyquote">
                                <p>
                                  <b>{newsItem.title}</b><br/>
                                  {newsItem.description}
                                  <br/>
                                  <cite title="Author" className="text-bold"><b>{newsItem.author}</b></cite> | <b>{newsItem.source.name}</b> | {Moment(newsItem.publishedAt).format('MMMM Do, YYYY')}
                                  <br/>
                                  <a href={newsItem.url} target="_blank" color="primary">Read more</a>
                                </p>
                                <footer>
                                  <div className="card-header-actions">
                                    <CBadge color={getBadge(newsItem.prediction)} className="float-right">{newsItem.prediction}</CBadge>
                                  </div>
                                </footer>
                              </blockquote>
                            </CCardBody>
                          </CCard>
                        </CCol>
                        ))}
                      </InfiniteScroll>
                    </CRow>
                  </CTabPane>
                  <CTabPane>
                    <CRow>
                      <CCol xs="12" sm="6" md="6">
                        <CCard>
                          <CCardHeader>
                            All News
                          </CCardHeader>
                          <CCardBody>
                            <CChartPie
                              type="pie"
                              datasets={[
                                {
                                  backgroundColor: colorsOps,
                                  data: dataOps
                                }
                              ]}
                              labels={labelsOps}
                              options={{
                                tooltips: {
                                  enabled: true
                                }
                              }}
                            />
                          </CCardBody>
                        </CCard>
                      </CCol>
                      <CCol xs="12" sm="6" md="6">
                        <CCard>
                          <CCardHeader>
                            Last 3 Months News
                          </CCardHeader>
                          <CCardBody>
                            <CChartDoughnut
                              type="doughnut"
                              datasets={[
                                {
                                  backgroundColor: colorsOpsLastMonths,
                                  data: dataOpsLastMonths
                                }
                              ]}
                              labels={labelsOpsLastMonths}
                              options={{
                                tooltips: {
                                  enabled: true
                                }
                              }}
                            />
                          </CCardBody>
                        </CCard>
                      </CCol>
                    </CRow>
                    <CRow>
                      <CCol xs="12" sm="12" md="12">
                        <CCard>
                          <CCardHeader>
                            News Per Month
                          </CCardHeader>
                          <CCardBody>
                            <CChartBar
                              type="bar"
                              datasets={[
                                {
                                  label: 'Positive',
                                  backgroundColor: '#2eb85c',
                                  data: posMonths
                                },
                                {
                                  label: 'Negative',
                                  backgroundColor: '#e55353',
                                  data: negMonths
                                }
                              ]}
                              labels="months"
                              options={{
                                tooltips: {
                                  enabled: true
                                }
                              }}
                            />
                          </CCardBody>
                        </CCard>
                      </CCol>
                    </CRow>
                    <CRow>
                      <CCol xs="12" sm="12" md="12">
                        <CCard>
                          <CCardHeader>
                            Last News
                          </CCardHeader>
                          <CCardBody>
                            <CChartLine
                              style={{height: '300px', marginTop: '40px'}}
                              datasets={defaultDatasets}
                              options={defaultOptions}
                              labels={labelsLines}
                            />
                          </CCardBody>
                        </CCard>
                      </CCol>
                    </CRow>
                  </CTabPane>
                </CTabContent>
              </CTabs>
            </CCardBody>
          </CCard>
        </CCol>
      </CRow>
    )
  }
}

export default SoceityDetails
