import React from 'react';
import './ParticipantTable.css';

interface Participant {
  name: string;
  id: string;
  receipt_number: string;
  amount: string;
}

interface ParticipantTableProps {
  participants: Participant[];
}

const ParticipantTable: React.FC<ParticipantTableProps> = ({ participants }) => {
  return (
    <div className="participant-table-container">
      <h4 className="table-title">פרטי משתתפים</h4>
      <div className="table-wrapper">
        <table className="participant-table">
          <thead>
            <tr>
              <th>שם</th>
              <th>תעודת זהות</th>
              <th>מספר קבלה</th>
              <th>סכום ששולם</th>
            </tr>
          </thead>
          <tbody>
            {participants.map((participant, index) => (
              <tr key={index}>
                <td>{participant.name || '-'}</td>
                <td>{participant.id || '-'}</td>
                <td>{participant.receipt_number || '-'}</td>
                <td>{participant.amount || '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ParticipantTable; 