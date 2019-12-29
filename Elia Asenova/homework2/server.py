import socket
from scripts import SequenceParser
from scripts import SequenceType

TCP_IP = '127.0.0.1'
TCP_PORT = 9001
BUFFER_SIZE = 1024

def sendSequence(conn, seq):
    file = open("data/sequence.txt", 'rb')
    while True:  
        data = file.read(BUFFER_SIZE)
        if not data:
            file.close()
            break
        else:
            conn.send(data)

def main():
    tcpsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpsocket.bind((TCP_IP, TCP_PORT))

    while True:
        tcpsocket.listen(3)
        (conn, (ip,port)) = tcpsocket.accept()
        seq_type = conn.recv(BUFFER_SIZE)
        if not seq_type:
            break

        seq_type = seq_type.decode()
        seq_parser = SequenceParser()
        sequence = ""
        if seq_type == "SequenceType.Fasta":
            with open("data/server_fasta.fa", 'r') as f:
                fasta_data = f.read()
            sequence = seq_parser.parse(SequenceType.Fasta, "fasta", fasta_data)
        elif seq_type == "SequenceType.FastQ":
            with open("data/server_fastq.fastq", 'r') as f:
                fastq_data = f.read()
            sequence = seq_parser.parse(SequenceType.FastQ, "fastq", fastq_data)

        with open("data/sequence.txt", 'w') as f:
            f.write(sequence[1])

        sendSequence(conn, sequence)

        conn.send('*'.encode())
        break

    conn.close()

if __name__=="__main__":
    main()
    