import React from 'react';
import { Modal, Button } from 'react-bootstrap';
import './modal.styl';


export default class MyModal extends React.Component {

  render() {

    let info = [];
    
    /** 
     * props.info is an array
     * [ {key:'time', value: 111}, 
         {key:'date' value:222},
         {key:'description' value:'stuffff'},
         {key:'url', value:'www.com'} ]
     */
    for (let i in this.props.data.info)
      if (this.props.data.info[i]) // If it has a value ie sometimes they don't set an endtime
        info.push(
          <div key={ this.props.data.info[i] }>
            <p>
              { this.props.data.info[i] }
            </p>
          </div>
        );


    return (
      <Modal show={ this.props.show } onHide={ this.props.close } >

        <Modal.Header closeButton>
          <Modal.Title>{ this.props.data.title }</Modal.Title>
        </Modal.Header>

        <Modal.Body>
          <div className="modal-section row">
            <div className="modal-picture">
              <img src={ this.props.data.img } height="200" width="250" />
            </div>

            <div className="modal-info">
                { info }
            </div>
          </div>

          <hr />
          
          <div className="modal-description">
            <h4>Description</h4>
            <p>{ this.props.data.description }</p>
          </div>

        </Modal.Body>
        <Modal.Footer>
          <Button onClick={this.props.close}>Close</Button>
        </Modal.Footer>
      </Modal>
    );
  }
}


