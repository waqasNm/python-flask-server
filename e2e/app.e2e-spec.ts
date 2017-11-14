import { AngularPythonPage } from './app.po';

describe('angular-python App', () => {
  let page: AngularPythonPage;

  beforeEach(() => {
    page = new AngularPythonPage();
  });

  it('should display welcome message', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('Welcome to app!');
  });
});
