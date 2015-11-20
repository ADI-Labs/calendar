import React from 'react';

// import Modal from 'components/lib/modal';

// import Navbar from 'components/Navbar';
// import Footer from 'components/Footer';

import 'bootstrap/dist/css/bootstrap.min.css'; // sketchy, inefficient
// import 'base.styl';

// import 'styles/main.css';
// import 'dev.css';



export default class App extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      showModal: false,
      modalData: {}
    };
  }

  componentDidMount() {


  }

  closeModal() {
    this.setState({ showModal: false });
  }
  openModal(data) {
    this.setState({ modalData: data, showModal: true });
  }


  render() {


    return (
      <div>
        {
          React.cloneElement(
            this.props.children,
            {
              myProp: "my prop!"
            }
          ) 
        }
      </div>
    );

    /*return (
      <div className="site-wrapper" >
        <Navbar />

        <Modal
          show={ this.state.showModal /* sketchy af ***}
          close={ this.closeModal.bind(this) }
          data={ this.state.modalData }
        />

        {
          React.cloneElement(
            this.props.children,
            {
              FB: this.state.FB,
              openModal: this.openModal.bind(this),
              closeModal: this.closeModal.bind(this),
              token: TOKEN
            }
          ) 
        }


        <div className="transparent-block" />

        <Footer />
      </div>
    );*/
  }
}






