import React, { lazy } from 'react'
import {
  CBadge,
  CButton,
  CButtonGroup,
  CCard,
  CCardBody,
  CCardFooter,
  CCardHeader,
  CCol,
  CProgress,
  CRow, CPagination, CAlert,
  CCallout, CWidgetProgress
} from '@coreui/react'
import CIcon from '@coreui/icons-react'

import { getStyle, hexToRgba } from '@coreui/utils/src'

import {
  CChartBar,
  CChartLine,
  CChartDoughnut,
  CChartRadar,
  CChartPie,
  CChartPolarArea
} from '@coreui/react-chartjs'

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

class Dashboard extends React.Component {
  constructor(props) {
    super(props);

    this.listNews = this.listNews.bind(this)
    this.getOpsDate = this.getOpsDate.bind(this)

    this.state = {
      societies: [],
      topNews: [],
      opsDate: [],
      dataOps: [],
      labelsOps: [],
      colorsOps: [],
      labelsLines: [],
      totalPos: 0,
      totalNeg: 0,
      totalNeu: 0,
    };
  }

  componentDidMount() {
    this.listNews()
    this.getAllOps()
  }

  componentDidUpdate() {
    //console.log(this.state.page + ':' + this.state.currentPage)
  }

  listSocieties() {
    const sector = this.state.sectors.find( sector => sector.slug === this.state.slug);
    societyService.getBySector(sector.title)
      .then(
        societies => {
          this.setState({
            societies: societies
          });
        },
        error => {
          this.setState({
            serverMessage: <CAlert color="danger">{error}</CAlert>
          });
        }
      );
  }

  listNews() {
    societyService.topNews()
      .then(
        news => {
          let top_news = [];
          news.slice(0, 6).map(function(item) {
            top_news.push(item)
          });
          this.setState({
            topNews: top_news
          });
        },
        error => {
          console.log(error)
        }
      );
  }

  getOpsDate(symbol) {
    if(this.state.opsDate.length <= 0) {
      societyService.getAllOpsDate()
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
            let tpos = 0
            let tneg = 0
            let tneu = 0
            dates.map(function(item, index) {
              ops[item].map(function(ob) {
                if(ob.predict == 'Positive') {
                  defaultDatasets[0].data.splice(index, 1, ob.total)
                  tpos = tpos + ob.total
                }
                if(ob.predict == 'Neutral') {
                  defaultDatasets[1].data.splice(index, 1, ob.total)
                  tneu = tneu + ob.total
                }
                if(ob.predict == 'Negative') {
                  defaultDatasets[2].data.splice(index, 1, ob.total)
                  tneg = tneg + ob.total
                }
              });
            });
            let maxs = [Math.max.apply(Math, defaultDatasets[0].data), Math.max.apply(Math, defaultDatasets[1].data), Math.max.apply(Math, defaultDatasets[2].data)]
            let max = Math.max.apply(Math, maxs)
            defaultOptions.scales.yAxes[0].ticks.max = max < 15 ? 15 : max
            this.setState({
              labelsLines: dates,
              totalPos: tpos,
              totalNeu: tneu,
              totalNeg: tneg
            });
          },
          error => {
            console.log({error})
          }
        );
    }
  }

  getAllOps(symbol) {
    this.getOpsDate(symbol);
  }

  render() {
    const { topNews, labelsOps, dataOps, colorsOps, labelsLines, totalNeg, totalNeu, totalPos } = this.state

    return (
      <>
        <CRow>
          { topNews && topNews.map((news, index) => (
          <CCol xs="12" sm="3" lg="2" key={index}>
            <CWidgetProgress text={news.ticker} header={`${Number(news.percent).toFixed(1)}%`}>
              <CProgress color="success" animated size="xs" className="my-2" value={news.percent}/>
            </CWidgetProgress>
          </CCol>
          ))}
        </CRow>
        <CCard>
          <CCardBody>
            <CRow>
              <CCol sm="5">
                <h4 id="traffic" className="card-title mb-0">Traffic</h4>
                <div className="small text-muted">Last 90 days</div>
              </CCol>
              <CCol sm="7" className="d-none d-md-block">
                <CButton color="primary" className="float-right">
                  <CIcon name="cil-cloud-download"/>
                </CButton>
              </CCol>
            </CRow>
            <CChartLine
              style={{height: '300px', marginTop: '40px'}}
              datasets={defaultDatasets}
              options={defaultOptions}
              labels={labelsLines}
            />
          </CCardBody>
          <CCardFooter>
            <CRow className="text-center">
              <CCol md sm="12" className="mb-sm-2 mb-0">
                <div className="text-muted">Positive</div>
                <strong>{totalPos} News</strong>
                <CProgress
                  className="progress-xs mt-2"
                  precision={1}
                  color="success"
                  value={40}
                />
              </CCol>
              <CCol md sm="12" className="mb-sm-2 mb-0">
                <div className="text-muted">Negative</div>
                <strong>{totalNeg} News</strong>
                <CProgress
                  className="progress-xs mt-2"
                  precision={1}
                  color="danger"
                  value={40}
                />
              </CCol>
              <CCol md sm="12" className="mb-sm-2 mb-0">
                <div className="text-muted">Neutral</div>
                <strong>{totalNeu} News</strong>
                <CProgress
                  className="progress-xs mt-2"
                  precision={1}
                  color="primary"
                  value={40}
                />
              </CCol>
            </CRow>
          </CCardFooter>
        </CCard>

        <CRow>
          <CCol>
            <CCard>
              <CCardHeader>
                Traffic {' & '} News
              </CCardHeader>
              <CCardBody>
                <CRow>
                  <CCol xs="12" md="12" xl="12">

                    <CRow>
                      <CCol sm="6">
                        <CCallout color="success">
                          <small className="text-muted">Positive News</small>
                          <br />
                          <strong className="h4">{totalPos}</strong>
                        </CCallout>
                      </CCol>
                      <CCol sm="6">
                        <CCallout color="danger">
                          <small className="text-muted">Negative News</small>
                          <br />
                          <strong className="h4">{totalNeg}</strong>
                        </CCallout>
                      </CCol>
                    </CRow>

                    <hr className="mt-0" />

                  </CCol>
                </CRow>

                <br />

                <table className="table table-hover table-outline mb-0 d-none d-sm-table">
                  <thead className="thead-light">
                    <tr>
                      <th>Ticker</th>
                      <th className="text-center">Positive share</th>
                      <th className="text-center">Positive articles</th>
                    </tr>
                  </thead>
                  <tbody>
                    {topNews && topNews.map((item, index) => (
                      <tr key={index}>
                        <td className="font-weight-bold">{item.ticker}</td>
                        <td className="text-center">{Number(item.percent).toFixed(1)}%</td>
                        <td className="text-center">{item.total}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>

              </CCardBody>
            </CCard>
          </CCol>
        </CRow>
      </>
    )
  }
}

export default Dashboard
