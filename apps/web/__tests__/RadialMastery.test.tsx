import { render, screen } from "@testing-library/react";
import { RadialMastery } from "../components/RadialMastery";
import { MasterySnapshot } from "../lib/adaptiveSample";

describe("RadialMastery", () => {
  const mockData: MasterySnapshot = {
    "ECG Basics": 50,
    Arrhythmias: 75,
  };

  it("renderiza o canvas com as dimensões corretas", () => {
    const testSize = 400;
    render(<RadialMastery data={mockData} size={testSize} />);

    const canvas = screen.getByRole("img"); // O canvas é tratado como uma imagem pelo testing-library

    expect(canvas).toBeInTheDocument();
    expect(canvas).toHaveAttribute("width", testSize.toString());
    expect(canvas).toHaveAttribute("height", testSize.toString());
  });

  it("renderiza com o tamanho padrão se nenhuma prop de tamanho for passada", () => {
    render(<RadialMastery data={mockData} />);

    const canvas = screen.getByRole("img");

    expect(canvas).toBeInTheDocument();
    expect(canvas).toHaveAttribute("width", "340"); // Valor padrão definido no componente
    expect(canvas).toHaveAttribute("height", "340");
  });
});
