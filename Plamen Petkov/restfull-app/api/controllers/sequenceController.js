'use strict';
const request = require('request')

const ENSEMBL_BASE_URL = "https://rest.ensembl.org"

exports.sequenceInfoById = function (req, res) {
    Promise.all([
        getSequenceForId(req.params.id),
        getExonsForId(req.params.id)
    ])
        .then(arr => {
            var resultingData = arr.reduce(((r, c) => Object.assign(r, c)), {})

            if (req.query) {
                if (req.query.gc_content) {
                    var gcCount = (resultingData.seq.match(/GC/g) || []).length
                    resultingData.gc_content = gcCount
                }

                if (req.query && req.query.swap) {

                    var swapSymbols = req.query.swap.split(":")
                    if (swapSymbols.length == 2) {
                        var swap1 = swapSymbols[0]
                        var swap2 = swapSymbols[1]

                        var tmpSeq = resultingData.seq
                        tmpSeq = tmpSeq.replace(new RegExp(swap1, "g"), "#")
                        tmpSeq = tmpSeq.replace(new RegExp(swap2, "g"), swap1)
                        tmpSeq = tmpSeq.replace(/#/g, swap2)

                        resultingData.swap_sequence = tmpSeq
                    }
                }
            }

            return res.json(resultingData)
        })
        .catch(err => {
            res.json(err)
        })
}

exports.exportToFormat = function (req, res) {
    if (req.query && req.query["content-type"]) {
        var contentType = req.query["content-type"]
        getSequenceForId(req.params.id)
            .then(data => {

                switch (contentType) {
                    case "fasta": {
                        return res.send(`>${data.description}\n${data.seq}`)
                    }
                    case "multi-fasta": {
                        return res.send(`>${data.description}\n${data.seq}`)
                    }
                    case "x-fasta": {
                        return res.json({
                            id: data.description,
                            seq: data.seq
                        })
                    }
                    default: return res.json("unsupported version please specify content-type in url: supported types are fasta/multi-fast/x-fasta")
                }
            })
    }
}

exports.home = (req, res) => {
    return res.send(`<h1>options are:</h1>
    /v1/sequence/gene/id/:id<br/>
    /v1/sequence/id/:id<br/>
    <h1>example:</h1>
    <a href="http://localhost:3003/v1/sequence/id/ENSG00000139618?content-type=x-fasta">http://localhost:3003/v1/sequence/id/ENSG00000139618?content-type=x-fasta</a><br/>
    <a href="http://localhost:3003/v1/sequence/gene/id/ENSG00000139618?swap=A:T&gc_content=1">http://localhost:3003/v1/sequence/gene/id/ENSG00000139618?swap=A:T&gc_content=1</a><br/>
    `)
  }

function getSequenceForId(geneId) {
    return new Promise((resolve, reject) => {
        let uri = `${ENSEMBL_BASE_URL}/sequence/id/${geneId}`
        const options = {
            url: uri,
            headers: {
                'Content-Type': 'application/json'
            }
        };
        request(options,
            (err, r, body) => {
                if (err) { return reject(err) }
                var responseJson = JSON.parse(body)
                return resolve({
                    "seq": responseJson.seq,
                    "description": responseJson.desc
                })
            })
    })
}

function getExonsForId(geneId) {
    return new Promise((resolve, reject) => {
        let uri = `${ENSEMBL_BASE_URL}/lookup/id/${geneId}?expand=1`
        const options = {
            url: uri,
            headers: {
                'Content-Type': 'application/json'
            }
        };
        request(options,
            (err, r, body) => {
                var responseJson = JSON.parse(body)
                if (err) { return reject(err) }

                if (responseJson.error) return resolve({})

                var data = []
                var promises = []

                //I don't want to make too many requests so I'll just take the first transcript
                responseJson.Transcript[0].Exon.forEach(exon => {
                    promises.push(
                        getSequenceForId(exon.id)
                            .then(exonSeq => {
                                data.push({
                                    start: exon.start,
                                    end: exon.end,
                                    id: exon.id,
                                    seq: exonSeq.seq
                                })
                            })
                            .catch(err => reject(err))
                    )
                })
                Promise.all(promises)
                    .then(_ => {
                        resolve({ "exons": data })
                    })
            })
    })
}