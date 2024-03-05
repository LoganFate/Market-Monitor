import { createBrowserRouter } from 'react-router-dom';
import LandingPage from '../components/LandingPage';
import HomePage from '../components/HomePage'
import StockDetailPage from '../components/StockDetailPage';
import Layout from './Layout';


export const router = createBrowserRouter([
  {
    element: <Layout />,
    children: [
      {
        path: "/",
        element: <LandingPage />,
      },
      {
        path: "/home",
        element: <HomePage />
      },
      {
        path: "/stock/:stockSymbol",
        element: <StockDetailPage />
      }
    ],
  },
]);
