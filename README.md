#Captain Nemo

## Inspiration

Manipulating data on-chain is a difficult task: smart contracts should handle as little data as possible and perform only the bare minimum logical operations. Uploading off-chain data to a smart contract is therefore not an easy process. 

A possible solution is to use an Oracle, a trusted off-chain agent that feeds external data to the contract.

We extend this concept and define a sort of oracle-on-steroids, that not only fetches data, but executes arbitrarily complex tasks and uploads the result. This oracle-on-steroids is a [fetch.ai](https://fetch.ai/) agent, [Captain Nemo](https://github.com/diffusioncon/Team-33).

## What it does
Captain Nemo is a bridge between on-chain smart contracts, off-chain [fetch.ai](https://fetch.ai/) agents and data on the [Ocean protocol](https://oceanprotocol.com/). 

The workflow is as follows:

1. A smart contract creates a query request on the `Submarine.sol` smart contract (the Submarine), by calling the function `createQuery`. The parameters are the address of the target fetch.ai agent, the command he should run, the did of the ocean resource and the identifier of the callback function to be called after the result is received.
2. The Submarine emits an event containing the query data
3. The agent logs events emitted from the Submarine and checks whether there is a request targeting them. 
4. The agent processes the request by first fetching the data from the [Ocean protocol](https://oceanprotocol.com/). Then they execute the requested command on the data.
5. The agent transmits the result to the Submarine. 
6. The Submarine calls the callback function on the original contract to set the result.

As an example, the agent `nemo.py` (Nemo) fetches data from the Ocean protocol, applies a machine learning algorithm and outputs the result.

## How we built it

`Submarine.sol` and `TestCase.sol` are two smart contracts written in solidity.
`nemo.py` is an agent written in python with the [fetch.ai](https://fetch.ai/) SDK.

## Challenges we ran into
Integrating all the various components from the different protocols has been the biggest challenge.

## What's next for Captain Nemo
A first step for Captain Nemo would be to integrate a payment system, where agents get paid after they process their data and users can rank agents according to the quality of the result.

A next step would be to integrate an agents market with a user interface, listing all agents addresses and possible commands. Users could then choose which agent best fits their needs and create queries accordingly.

## Links

`Submarine.sol` is deployed on the [Nile testnet](https://nile.dev-ocean.com) at `0x7d5158372BC13D1bA316b44B9002821BE46652F5`.
`TestCase.sol` is deployed on the [Nile testnet](https://nile.dev-ocean.com) at `0xb930AF9aDfe58029B135EA2949b591C46849de4c`.