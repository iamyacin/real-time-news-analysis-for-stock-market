import React from 'react'
import { Link } from 'react-router-dom'
import {
  CButton,
  CCard,
  CCardBody,
  CCardGroup,
  CCol,
  CContainer,
  CForm,
  CInput,
  CInputGroup,
  CInputGroupPrepend,
  CInputGroupText,
  CRow,
  CAlert
} from '@coreui/react'
import CIcon from '@coreui/icons-react'

import { authenticationService } from '../../../_services/authentication.service'
import * as Yup from 'yup'

class Login extends React.Component {
  constructor(props) {
    super(props);

    this.onChangeEmail = this.onChangeEmail.bind(this);
    this.onChangePassword = this.onChangePassword.bind(this);
    this.login = this.login.bind(this);

    this.state = {
      email: "",
      password: "",
      submitted: false,
      error: "",
      serverMessage: "",
      successMessage: "",
      validatorMessage: ""
    };

    // redirect to home if already logged in
    if (authenticationService.currentUserValue) {
      this.props.history.push('/');
    }
  }

  componentDidMount() {
    //console.log(this.props.term);
  }

  onChangeEmail(e) {
    this.setState({
      email: e.target.value
    });
  }

  onChangePassword(e) {
    this.setState({
      password: e.target.value
    });
  }

  login() {
    let email = this.state.email
    let password = this.state.password
    //setStatus();
    authenticationService.login(email, password)
      .then(
        user => {
          this.setState({
            successMessage: <CAlert color="success">{"Congradulations you are logged in."}</CAlert>,
            serverMessage: ""
          });
          const { from } = this.props.location.state || { from: { pathname: "/" } };
          //this.props.history.push(from);
          window.location.href = "/dashboard";
        },
        error => {
          this.setState({
            serverMessage: <CAlert color="danger">{error}</CAlert>
          });
        }
      );
  }

  render() {
    const { email, password, submited, serverMessage, successMessage } = this.state;

    return (
      <div className="c-app c-default-layout flex-row align-items-center">
        <CContainer>
          <CRow className="justify-content-center">
            <CCol md="8">
              <CCardGroup>
                <CCard className="p-4">
                  <CCardBody>
                    { serverMessage }
                    { successMessage }
                    <CForm>
                      <h1>Login</h1>
                      <p className="text-muted">Sign In to your account</p>
                      <CInputGroup className="mb-3">
                        <CInputGroupPrepend>
                          <CInputGroupText>
                            <CIcon name="cil-user"/>
                          </CInputGroupText>
                        </CInputGroupPrepend>
                        <CInput type="text" placeholder="Username" autoComplete="username" value={email} required="required" onChange={this.onChangeEmail} />
                      </CInputGroup>
                      <CInputGroup className="mb-4">
                        <CInputGroupPrepend>
                          <CInputGroupText>
                            <CIcon name="cil-lock-locked"/>
                          </CInputGroupText>
                        </CInputGroupPrepend>
                        <CInput type="password" placeholder="Password" autoComplete="current-password" required="required" value={password} onChange={this.onChangePassword}/>
                      </CInputGroup>
                      <CRow>
                        <CCol xs="6">
                          <CButton onClick={this.login} color="primary" className="px-4">Login</CButton>
                        </CCol>
                        <CCol xs="6" className="text-right">
                          <CButton color="link" className="px-0">Forgot password?</CButton>
                        </CCol>
                      </CRow>
                    </CForm>
                  </CCardBody>
                </CCard>
                <CCard className="text-white bg-primary py-5 d-md-down-none" style={{width: '44%'}}>
                  <CCardBody className="text-center">
                    <div>
                      <h2>Sign up</h2>
                      <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut
                        labore et dolore magna aliqua.</p>
                      <Link to="/register">
                        <CButton color="primary" className="mt-3" active tabIndex={-1}>Register Now!</CButton>
                      </Link>
                    </div>
                  </CCardBody>
                </CCard>
              </CCardGroup>
            </CCol>
          </CRow>
        </CContainer>
      </div>
    )
  }
}

export default Login
