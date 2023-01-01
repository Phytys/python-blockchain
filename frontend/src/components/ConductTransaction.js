import React, {useState, useEffect} from "react";
import {Link} from 'react-router-dom';
import {FormGroup, FormControl, Button} from 'react-bootstrap';
import { responsivePropType } from "react-bootstrap/esm/createUtilityClasses";
import {API_BASE_URL} from '../config';
import history from "../history";

function ConductTransaction() {
    const [amount, setAmount] = useState(0);
    const [recipient, setRecipient] = useState('');
    const [knownAddresses, setKnownAddresses] = useState(['']);

    useEffect(() => {
        fetch(`${API_BASE_URL}/known-addresses`)
        .then(response => response.json())
        .then(json => setKnownAddresses(json));
    }, [])

    const updateRecipient = event => {
        setRecipient(event.target.value);
    }
    const updateAmount = event => {
        setAmount(Number(event.target.value));
    }

    const submitTransaction = () => {
        fetch(
            `${API_BASE_URL}/wallet/transact`,
            {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({recipient, amount})
            }
         )
            .then(response => response.json())
            .then(json => {
                console.log('submittransaction json', json);
                alert('Success!');

                history.push('/transaction-pool');
            })

    }

    // JSX
    return (
        <div className='ConductTransaction'>
            <Link to='/'>Home</Link>
            <hr/>
            <h3>Conduct a Transaction</h3>
            <br/>
            <FormGroup>
                <FormControl
                inputMode='text'
                placeholder="recipient"
                value={recipient}
                onChange={updateRecipient}
                />
            </FormGroup>
            <FormGroup>
                <FormControl
                input='number'
                placeholder='amount'
                onChange = {updateAmount}
                />
            </FormGroup>
            <div>
                <Button
                    variant='danger'
                    // onClick fires a callbackfunction
                    onClick={submitTransaction}
                    >
                    Submit
                </Button>
            </div>
            <br/>
            <h4>Known Addresses</h4>
            <div>
                {
                    // .. for each known adress
                    knownAddresses.map((knownAddress, i) => (
                        <span key={knownAddress}>
                            <u>{knownAddress}</u>{i !== knownAddresses.length -1 ? ', ' : ''}
                        </span>
                    ))
                }
            </div>
        </div>
    )
}

export default ConductTransaction;