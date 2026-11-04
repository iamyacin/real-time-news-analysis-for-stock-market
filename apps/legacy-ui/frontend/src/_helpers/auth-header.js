import { authenticationService } from '../_services';

export function authHeader() {
    // return authorization header with jwt token
    const currentUser = authenticationService.currentUserValue;
    if (currentUser && currentUser.accessToken) {
      //console.log(currentUser)
      return {
        Authorization: `Bearer ${currentUser.accessToken}`,
        ContentType: 'application/json',
        AccessControlAllowOrigin: '*',
        ChangeOrigin: true
      };
    } else {
      return {};
    }
}
