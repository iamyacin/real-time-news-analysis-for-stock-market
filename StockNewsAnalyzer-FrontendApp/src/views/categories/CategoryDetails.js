import React, { useState, useEffect } from 'react'
import { history } from '../../_helpers';
import {
  CBadge,
  CCard,
  CCardBody,
  CCardHeader,
  CCol,
  CDataTable,
  CRow,
  CPagination, CAlert
} from '@coreui/react'

import {societyService} from "../../_services"

const getBadge = status => {
  switch (status) {
    case 'Active': return 'success'
    case 'Inactive': return 'secondary'
    case 'Pending': return 'warning'
    case 'Banned': return 'danger'
    default: return 'primary'
  }
}

const slugify = (string) => {
  const a = 'àáäâãåèéëêìíïîòóöôùúüûñçßÿœæŕśńṕẃǵǹḿǘẍźḧ·/_,:;'
  const b = 'aaaaaaeeeeiiiioooouuuuncsyoarsnpwgnmuxzh------'
  const p = new RegExp(a.split('').join('|'), 'g')
  return string.toString().toLowerCase()
      .replace(/\s+/g, '-') // Replace spaces with -
      .replace(p, c => b.charAt(a.indexOf(c))) // Replace special characters in a with b
      .replace(/&/g, '-and-') // Replace & with ‘and’
      .replace(/[^\w-]+/g, '') // Remove all non-word characters such as spaces or tabs
      .replace(/--+/g, '-') // Replace multiple — with single -
      .replace(/^-+/, '') // Trim — from start of text
      .replace(/-+$/, ''); // Trim — from end of text
}

class CategoryDetails extends React.Component {
  constructor(props) {
    super(props);

    this.listSocieties = this.listSocieties.bind(this)
    this.pageChange = this.pageChange.bind(this)
    this.setPage = this.setPage.bind(this)
    this.listSectors = this.listSectors.bind(this)

    this.state = {
      societies: [],
      sectors: [],
      queryPage: "",
      currentPage: 1,
      page: 1,
      slug: ''
    };
  }

  componentDidMount() {
    const { match: { params } } = this.props
    this.setState({slug: params.id})
    this.listSectors()
    this.state.queryPage = window.location.search.match(/page=([0-9]+)/, '')
    this.state.currentPage = Number(this.state.queryPage && this.state.queryPage[1] ? this.state.queryPage[1] : 1)
    this.state.currentPage !== this.state.page && this.setPage(this.state.currentPage)
  }

  componentDidUpdate() {
    //console.log(this.state.page + ':' + this.state.currentPage)
    this.state.currentPage !== this.state.page && this.setPage(this.state.currentPage)
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

  listSectors() {
    societyService.getSectors()
      .then(
        sectors => {
          let se = [];
          sectors.map(function(item) {
            let slug = slugify(item)
            se.push({slug: slug, title: item})
          });
          console.log(se)
          this.setState({
            sectors: se
          });
          this.listSocieties()
        },
        error => {
          console.log(error)
        }
      );
  }

  pageChange(newPage) {
    this.state.currentPage !== newPage && history.push(`/categories/${this.state.slug}?page=${newPage}`)
    this.state.page = this.state.currentPage !== newPage ? newPage : this.state.currentPage
    this.state.currentPage = this.state.currentPage !== newPage ? newPage : this.state.currentPage
  }

  setPage(curPage) {
    this.state.page = curPage
  }

  render() {
    const { queryPage, currentPage, page, societies } = this.state

    /*useEffect(() => {
      currentPage !== page && this.setPage(currentPage)
    }, [currentPage, page])*/

    return (
      <CRow>
        <CCol xl={12}>
          <CCard>
            <CCardHeader>
              <span className="text-center font-weight-bold">Societies</span>
            </CCardHeader>
            <CCardBody>
              <CRow>
                <CCol xs="12" sm="12" md="12">
                  <CDataTable
                    items={societies}
                    fields={[
                      { key: 'symbol', _classes: 'font-weight-bold' },
                      'logo_url', 'shortName', 'country', 'industry', 'sector', 'currency'
                    ]}
                    hover
                    striped
                    addTableClasses={"mb-0 d-none d-sm-table table-outline"}
                    itemsPerPage={10}
                    activePage={page}
                    clickableRows
                    onRowClick={(item) => history.push(`/societies/${item.id}`)}
                    scopedSlots = {{
                      'logo_url':
                        (item)=>(
                          <td>
                            <img width={45} src={item.logo_url} className="c-icon c-icon-custom-size" />
                          </td>
                        )
                    }}
                  />
                  <CPagination
                    activePage={page}
                    onActivePageChange={this.pageChange}
                    pages={10}
                    doubleArrows={false}
                    align="center"
                  />
                </CCol>
              </CRow>
            </CCardBody>
          </CCard>
        </CCol>
      </CRow>
    )
  }
}

export default CategoryDetails
