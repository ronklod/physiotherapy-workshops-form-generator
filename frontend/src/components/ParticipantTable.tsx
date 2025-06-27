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
              {/* Hebrew RTL Order: Name (rightmost) → ID → Receipt → Amount (leftmost) */}
              <th>שם</th>
              <th>ת.ז</th>
              <th>מס' קבלה</th>
              <th>סכום</th>
            </tr>
          </thead>
          <tbody>
            {participants.map((participant, index) => (
              <tr key={index}>
                {/* Name column (rightmost in display) */}
                <td>{participant.name || '-'}</td>
                {/* ID column */}
                <td>{participant.id || '-'}</td>
                {/* Receipt Number column */}
                <td>{participant.receipt_number || '-'}</td>
                {/* Amount column (leftmost in display) */}
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