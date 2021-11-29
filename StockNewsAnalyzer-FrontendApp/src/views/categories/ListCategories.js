import React, { useState, useEffect } from 'react'
import { useHistory, useLocation } from 'react-router-dom'
import { history } from '../../_helpers'
import {
  CBadge,
  CCard,
  CCardBody,
  CCardHeader,
  CCol,
  CDataTable,
  CRow, CLink,
  CPagination
} from '@coreui/react'

import {societyService} from "../../_services"

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

class ListCategories extends React.Component {
  constructor(props) {
    super(props);

    this.listSectors = this.listSectors.bind(this)

    this.state = {
      sectors: [],
      queryPage: "",
      currentPage: 1,
      page: 1
    };
  }

  componentDidMount() {
    this.listSectors()
  }

  componentDidUpdate() {
    //console.log(this.state.page + ':' + this.state.currentPage)
  }

  listSectors() {
    societyService.getSectors()
      .then(
        sectors => {
          this.setState({
            sectors: sectors
          });
        },
        error => {
          console.log(error)
        }
      );
  }

  render() {
    const { sectors } = this.state

    return (
      <CRow>
        <CCol xl={12}>
          <CCard>
            <CCardHeader>
              <span className="text-center font-weight-bold">All Sectors</span>
            </CCardHeader>
            <CCardBody>
              <CRow>
                { sectors && sectors.map((sector, index) => (
                <CCol xs="12" sm="4" md="4" key={index}>
                  <CLink
                    to={`/categories/${slugify(sector)}`}
                  >
                    <CCard color="success" className="text-white text-center">
                      <CCardBody>
                        <blockquote className="card-bodyquote">
                          <h6>{sector}</h6>
                        </blockquote>
                      </CCardBody>
                    </CCard>
                  </CLink>
                </CCol>
                ))}
              </CRow>
            </CCardBody>
          </CCard>
        </CCol>
      </CRow>
    )
  }
}

export default ListCategories
