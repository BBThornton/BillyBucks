# BillyBucks: A Framework for Pay-as-you-go Monetisation of Digital Data Streams
## Abstract
The growth of cryptocurrencies has facilitated new economic tools which have revolutionised
the management of ownership and transactions relating to digital assets. By utilising the browser-
based mining of cryptocurrencies there is the potential to support a pay-as-you-go alternative for
the monetisation of open digital data streams. However due the mining difficult of Proof-of-Work
mining many low client powered devices are unable to generate significant sums of cryptocurrency
through the mining process making browser based mining infeasible as an alternative to traditional
monetisation methods. This project proposes and implements a balanced mining framework which
aims to support browser-based mining as a form of digital data steam monetisation by improving
low powered miners’ ability to generate cryptocurrency during the mining process. The balanced
mining framework consists of a specially created dedicated permissioned cryptocurrency, a mining
pool with novel operating behaviours and a JavaScript mining dependency. These components are
able to reduce the performance and currency generation inequality between high and low hashrate
miners by decoupling device hashrate from the reward generation process.
This framework is able to improve the reward generation rates of low powered miners and thus
greatly increases the feasibility of browser-based mining as a form of pay-as-you-go digital data
stream monetisation.

## Projects
The source code for this project is seperated between multiple repositories.
### BillyBucks Blockchain
The BillyBucks blockchain is the repository which contains a fork of the TurtleCoin code and also contains the information to make further forks of the code. Including the command necessary to deploy the blockchain.

**Link:** [https://github.com/BBThornton/BillyBucksBlockchain](https://github.com/BBThornton/BillyBucksBlockchain)

### BillyBucks Balanced Mining Pool
This repository contains the code responsible for the balanced mining pool and is used with the BillyBucks blockchain to allow miners to join the mining process in the permissioned blockchain.

**Link:** [https://github.com/BBThornton/BillyBucksMiningPool](https://github.com/BBThornton/BillyBucksMiningPool)

### BillyBucks JavaScript Web Miner and Manager
This repository contains the alter code of a Javascript based miner and the miner manager server. It has been updated to both suport the new TurtleCoin hashing algorithm (Chukwa v2) and also recognise and support the "null"/"pause" job of the BillyBucks Mining pool.

**Link:** [https://github.com/BBThornton/BillyBucksWebMiner](https://github.com/BBThornton/BillyBucksWebMiner)

### Demo Website
The demo website was used during the demo video and provides a simple example on how to include the WebMining dependency into a website to join the mining network.
The code for this is included in this repository in the WebDemo folder.

### Simulation Code
A python simulation was also created as part of the report process. This simulation was used to generate the figures used as part of the report/thesis. This code is not "beautified" and is raw, please don't judge the code too harshly.

This code is included in the Simulation Folder of this repository.