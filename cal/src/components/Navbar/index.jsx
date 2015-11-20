import React from 'react';
import { Navbar, NavBrand, Nav, NavItem, MenuItem } from 'react-bootstrap';
import { IndexLinkContainer, LinkContainer } from 'react-router-bootstrap';

import './bootstrap-override.styl';


export default class Navigation extends React.Component {
  render() {
    return (
      <Navbar fixedTop>
        <Navbar.Header>
          <Navbar.Brand>
            <IndexLinkContainer to="/">
              <a href="#">Sabor</a>
            </IndexLinkContainer>
          </Navbar.Brand>
          <Navbar.Toggle />
        </Navbar.Header>
        <Navbar.Collapse>
          <Nav pullRight>
            <IndexLinkContainer to="/">
              <NavItem eventKey={1} href="#">Home</NavItem>
            </IndexLinkContainer>
            <LinkContainer to="events">
              <NavItem eventKey={2} href="#">Events</NavItem>
            </LinkContainer>
            <LinkContainer to="team">
              <NavItem eventKey={3} href="#">Team</NavItem>
            </LinkContainer>
            <LinkContainer to="releve">
              <NavItem eventKey={4} href="#">Releve</NavItem>
            </LinkContainer>
          </Nav>
        </Navbar.Collapse>
      </Navbar>
    );
  }
}
