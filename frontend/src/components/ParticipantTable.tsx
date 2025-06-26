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
              {/* Hebrew RTL Order: Reverse order for proper RTL display */}
              {/* Amount column will appear leftmost */}
              <th>סכום</th>
              {/* Receipt Number column */}
              <th>מס' קבלה</th>
              {/* ID column */}
              <th>ת.ז</th>
              {/* Name column will appear rightmost */}
              <th>שם</th>
            </tr>
          </thead>
          <tbody>
            {participants.map((participant, index) => (
              <tr key={index}>
                {/* Amount column (leftmost in display) */}
                <td>{participant.amount || '-'}</td>
                {/* Receipt Number column */}
                <td>{participant.receipt_number || '-'}</td>
                {/* ID column */}
                <td>{participant.id || '-'}</td>
                {/* Name column (rightmost in display) */}
                <td>{participant.name || '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ParticipantTable; 