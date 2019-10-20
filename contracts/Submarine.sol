pragma solidity ^0.5.0;

/**
* Submarine
*
* MIT License
* 
* Copyright (c) 2019 Alessandro Ricottone
* 
* Permission is hereby granted, free of charge, to any person obtaining a copy
* of this software and associated documentation files (the "Software"), to deal
* in the Software without restriction, including without limitation the rights
* to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
* copies of the Software, and to permit persons to whom the Software is
* furnished to do so, subject to the following conditions:
* 
* The above copyright notice and this permission notice shall be included in all
* copies or substantial portions of the Software.
* 
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
* IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
* FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
* AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
* LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
* OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
* SOFTWARE.
 */
contract Submarine {

    event QueryCreated(address agentAddress, string command, bytes oceanDid, address queryContract);
    mapping (address => mapping (address => bytes4) ) public queryBook;
    mapping (address => mapping (address => bytes4) ) public paymentsBook;
    
    
    /**
    * @dev Emits query with passed parameters. Event log is then intercepted from the off-chain agent that performs the query and call the updateQuery function.
    * @param _agentAddress The Fetch.ai agent address (identifier).
    * @param _command The command to be run by the agent.
    * @param _oceanDid The data identifier for the Ocean protocol.
    * @param _callback The callback method to call on the query contract.
    */
    function createQuery (address _agentAddress, string calldata _command, bytes calldata _oceanDid, bytes4 _callback) external {
        //require(queryBook[msg.sender][_agentAddress] == "");
        emit QueryCreated(_agentAddress, _command, _oceanDid, msg.sender);
        queryBook[msg.sender][_agentAddress] = _callback;
    }

    /**
    * @dev Updates the contract that created the query by calling the specified callback function and passing the result as a parameter.
    * @param _queryContract The address of the contract that created the query.
    * @param _result The result as a dynamic sized array (we use function overloading to catch many possible variable types)
    */
    function updateQuery(address _queryContract,  uint[] memory _result) public returns (bool){
        bytes4 _callback = queryBook[_queryContract][msg.sender];
        require (_callback != "");
        (bool status,) = _queryContract.call(abi.encodePacked(_callback, uint(32), uint(_result.length), _result));
        queryBook[_queryContract][msg.sender] = "";
        require(status, "Failed callback");
        return true;
    }

}
