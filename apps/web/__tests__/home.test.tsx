import { render, screen } from '@testing-library/react';

// Mock next-intl
jest.mock('next-intl', () => ({
  useTranslations: () => (key: string) => {
    const messages: { [key: string]: string } = {
      'home.title': 'MEGA',
      'home.intro': 'Plataforma modular de educação médica.',
      'nav.modules': 'Explorar Módulos',
      'nav.adaptive': 'Adaptive Dashboard'
    };
    return messages[key] || key;
  }
}));

// Mock the loadMessages function
jest.mock('../lib/loadMessages', () => ({
  loadMessages: jest.fn(() => Promise.resolve({}))
}));

import Home from '../pages/index';

describe('Home', () => {
  it('renderiza título', () => {
    render(<Home />);
    expect(screen.getByText('MEGA')).toBeInTheDocument();
  });
  
  it('renderiza conteúdo de introdução', () => {
    render(<Home />);
    expect(screen.getByText('Plataforma modular de educação médica.')).toBeInTheDocument();
  });
});