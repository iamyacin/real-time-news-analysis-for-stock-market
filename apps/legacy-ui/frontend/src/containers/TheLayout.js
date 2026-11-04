import React from 'react'
import { Redirect } from 'react-router-dom'
import {
  TheContent,
  TheSidebar,
  TheFooter,
  TheHeader
} from './index'

import {authenticationService} from "../_services";

const currentUser = authenticationService.currentUserValue;

const TheLayout = () => {
  return (
    <div className="c-app c-default-layout">
      <TheSidebar/>
      <div className="c-wrapper">
        <TheHeader/>
        <div className="c-body">
          { currentUser ? (
            <TheContent/>
          ) : (
            <Redirect from="/" to="/login" />
          )}
        </div>
        <TheFooter/>
      </div>
    </div>
  )
}

export default TheLayout
