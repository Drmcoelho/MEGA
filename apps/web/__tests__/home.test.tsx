import { render, screen } from "@testing-library/react";
import Home from "../pages/index";

describe("Home", () => {
  it("renderiza título", () => {
    render(<Home />);
    expect(screen.getByText(/MEGA/i)).toBeInTheDocument();
  });
});
