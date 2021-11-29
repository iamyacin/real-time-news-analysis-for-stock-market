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
            <CWidgetProgress text={news.ticker} header={`${news.percent}%`}>
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
                <div className="small text-muted">November 2020</div>
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
                          <strong className="h4">9,123</strong>
                        </CCallout>
                      </CCol>
                      <CCol sm="6">
                        <CCallout color="danger">
                          <small className="text-muted">Negative News</small>
                          <br />
                          <strong className="h4">22,643</strong>
                        </CCallout>
                      </CCol>
                    </CRow>

                    <hr className="mt-0" />

                    <div className="progress-group mb-4">
                      <div className="progress-group-prepend">
                        <span className="progress-group-text">
                          Monday
                        </span>
                      </div>
                      <div className="progress-group-bars">
                        <CProgress className="progress-xs" color="success" value="34" />
                        <CProgress className="progress-xs" color="danger" value="78" />
                      </div>
                    </div>
                    <div className="progress-group mb-4">
                      <div className="progress-group-prepend">
                        <span className="progress-group-text">
                        Tuesday
                        </span>
                      </div>
                      <div className="progress-group-bars">
                        <CProgress className="progress-xs" color="success" value="56" />
                        <CProgress className="progress-xs" color="danger" value="94" />
                      </div>
                    </div>
                    <div className="progress-group mb-4">
                      <div className="progress-group-prepend">
                        <span className="progress-group-text">
                        Wednesday
                        </span>
                      </div>
                      <div className="progress-group-bars">
                        <CProgress className="progress-xs" color="success" value="12" />
                        <CProgress className="progress-xs" color="danger" value="67" />
                      </div>
                    </div>
                    <div className="progress-group mb-4">
                      <div className="progress-group-prepend">
                        <span className="progress-group-text">
                        Thursday
                        </span>
                      </div>
                      <div className="progress-group-bars">
                        <CProgress className="progress-xs" color="success" value="43" />
                        <CProgress className="progress-xs" color="danger" value="91" />
                      </div>
                    </div>
                    <div className="progress-group mb-4">
                      <div className="progress-group-prepend">
                        <span className="progress-group-text">
                        Friday
                        </span>
                      </div>
                      <div className="progress-group-bars">
                        <CProgress className="progress-xs" color="success" value="22" />
                        <CProgress className="progress-xs" color="danger" value="73" />
                      </div>
                    </div>
                    <div className="progress-group mb-4">
                      <div className="progress-group-prepend">
                        <span className="progress-group-text">
                        Saturday
                        </span>
                      </div>
                      <div className="progress-group-bars">
                        <CProgress className="progress-xs" color="success" value="53" />
                        <CProgress className="progress-xs" color="danger" value="82" />
                      </div>
                    </div>
                    <div className="progress-group mb-4">
                      <div className="progress-group-prepend">
                        <span className="progress-group-text">
                        Sunday
                        </span>
                      </div>
                      <div className="progress-group-bars">
                        <CProgress className="progress-xs" color="success" value="9" />
                        <CProgress className="progress-xs" color="danger" value="69" />
                      </div>
                    </div>
                    <div className="legend text-center">
                      <small>
                        <sup className="px-1"><CBadge shape="pill" color="success">&nbsp;</CBadge></sup>
                        Positive News
                        &nbsp;
                        <sup className="px-1"><CBadge shape="pill" color="danger">&nbsp;</CBadge></sup>
                        Negative News
                      </small>
                    </div>
                  </CCol>
                </CRow>

                <br />

                <table className="table table-hover table-outline mb-0 d-none d-sm-table">
                  <thead className="thead-light">
                    <tr>
                      <th className="text-center">Logo</th>
                      <th>Society</th>
                      <th className="text-center">Country</th>
                      <th>Activity</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td className="text-center">
                        <span>
                          <img src="/imgs/svg/brand/cib-amazon.svg" className="c-icon c-icon-custom-size" />
                        </span>
                      </td>
                      <td>
                        <div>Amazon</div>
                        <div className="small text-muted">
                          <span>AMZ</span> | Created: Jan 1, 2015
                        </div>
                      </td>
                      <td className="text-center">
                        <CIcon height={25} name="cif-us" title="us" id="us" />
                      </td>
                      <td>
                        <div className="small text-muted">Ecommerce</div>
                      </td>
                    </tr>
                    <tr>
                      <td className="text-center">
                        <span>
                          <img src="/imgs/svg/brand/cib-amazon.svg" className="c-icon c-icon-custom-size" />
                        </span>
                      </td>
                      <td>
                        <div>Amazon</div>
                        <div className="small text-muted">
                          <span>AMZ</span> | Created: Jan 1, 2015
                        </div>
                      </td>
                      <td className="text-center">
                        <CIcon height={25} name="cif-us" title="us" id="us" />
                      </td>
                      <td>
                        <div className="small text-muted">Ecommerce</div>
                      </td>
                    </tr>
                    <tr>
                      <td className="text-center">
                        <span>
                          <img src="/imgs/svg/brand/cib-amazon.svg" className="c-icon c-icon-custom-size" />
                        </span>
                      </td>
                      <td>
                        <div>Amazon</div>
                        <div className="small text-muted">
                          <span>AMZ</span> | Created: Jan 1, 2015
                        </div>
                      </td>
                      <td className="text-center">
                        <CIcon height={25} name="cif-us" title="us" id="us" />
                      </td>
                      <td>
                        <div className="small text-muted">Ecommerce</div>
                      </td>
                    </tr>
                    <tr>
                      <td className="text-center">
                        <span>
                          <img src="/imgs/svg/brand/cib-amazon.svg" className="c-icon c-icon-custom-size" />
                        </span>
                      </td>
                      <td>
                        <div>Amazon</div>
                        <div className="small text-muted">
                          <span>AMZ</span> | Created: Jan 1, 2015
                        </div>
                      </td>
                      <td className="text-center">
                        <CIcon height={25} name="cif-us" title="us" id="us" />
                      </td>
                      <td>
                        <div className="small text-muted">Ecommerce</div>
                      </td>
                    </tr>
                    <tr>
                      <td className="text-center">
                        <span>
                          <img src="/imgs/svg/brand/cib-amazon.svg" className="c-icon c-icon-custom-size" />
                        </span>
                      </td>
                      <td>
                        <div>Amazon</div>
                        <div className="small text-muted">
                          <span>AMZ</span> | Created: Jan 1, 2015
                        </div>
                      </td>
                      <td className="text-center">
                        <CIcon height={25} name="cif-us" title="us" id="us" />
                      </td>
                      <td>
                        <div className="small text-muted">Ecommerce</div>
                      </td>
                    </tr>
                    <tr>
                      <td className="text-center">
                        <span>
                          <img src="/imgs/svg/brand/cib-amazon.svg" className="c-icon c-icon-custom-size" />
                        </span>
                      </td>
                      <td>
                        <div>Amazon</div>
                        <div className="small text-muted">
                          <span>AMZ</span> | Created: Jan 1, 2015
                        </div>
                      </td>
                      <td className="text-center">
                        <CIcon height={25} name="cif-us" title="us" id="us" />
                      </td>
                      <td>
                        <div className="small text-muted">Ecommerce</div>
                      </td>
                    </tr>
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
