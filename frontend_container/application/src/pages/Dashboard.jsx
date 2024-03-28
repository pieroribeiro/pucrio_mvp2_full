import React from 'react';

import DashboardCotationBitcoin from '../partials/dashboard/DashboardCotationBitcoin';
import DashboardCotationEthereum from '../partials/dashboard/DashboardCotationEthereum';
import DashboardCotationSolana from '../partials/dashboard/DashboardCotationSolana';
import DashboardCotation01 from '../partials/dashboard/DashboardCotation01';
import DashboardCotation02 from '../partials/dashboard/DashboardCotation02';
import DashboardCotation03 from '../partials/dashboard/DashboardCotation03';
import DashboardNews from '../partials/dashboard/DashboardNews';

function Dashboard() {

  return (
    <div className="flex h-screen overflow-hidden">
      <div className="relative flex flex-col flex-1 overflow-y-auto overflow-x-hidden">
        <main>
          <div className="px-4 sm:px-6 lg:px-8 py-8 w-full max-w-9xl mx-auto">
            <div className="grid grid-cols-12 gap-6">
              <DashboardCotationBitcoin />
              <DashboardCotationEthereum />
              <DashboardCotationSolana />
              <DashboardCotation01 />
              <DashboardCotation02 />
              <DashboardCotation03 />
              <DashboardNews />
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}

export default Dashboard;