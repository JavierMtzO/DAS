import { useEffect, useState } from 'react';
import Container from 'react-bootstrap/Container';

export default function Dashboard() {

  return (
    <Container fluid className='full-page-with-nav'>
      <div className='row mt-3 mt-md-5'>
        <h2>Dashboard</h2>
      </div>
      <hr />
    </Container>
  );
}