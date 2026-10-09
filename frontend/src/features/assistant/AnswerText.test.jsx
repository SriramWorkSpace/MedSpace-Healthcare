import { fireEvent, render, screen } from "@testing-library/react";
import { AnswerText } from "./AnswerText";
import { normalizeAnswer } from "./answerFormat";

describe("AnswerText", () => {
  it("renders bold without showing the asterisks", () => {
    const { container } = render(<AnswerText text="- Follow a **low-salt, low-sugar diet** [1]" />);
    expect(container.textContent).not.toContain("**");
    expect(screen.getByText("low-salt, low-sugar diet").tagName).toBe("STRONG");
  });

  it("turns the model's 【n】 citations into source buttons", () => {
    const onCite = vi.fn();
    render(<AnswerText text={"- Avoid sugary drinks 【2】【6†L3-L5】"} onCite={onCite} />);
    expect(screen.queryByText(/【|】/)).toBeNull();
    fireEvent.click(screen.getByRole("button", { name: "Source 6" }));
    expect(onCite).toHaveBeenCalledWith(6);
    expect(screen.getByRole("button", { name: "Source 2" })).toBeInTheDocument();
  });

  it("hides an unpaired ** while the answer is still streaming", () => {
    const { container } = render(<AnswerText text="Take **Metfor" streaming />);
    expect(container.textContent).toBe("Take Metfor");
  });

  it("renders numbered lists and headings without their markers", () => {
    const { container } = render(
      <AnswerText text={"### Your medicines\n1. Metformin [1]\n2. Atorvastatin [2]"} />,
    );
    expect(container.querySelector("ol").children).toHaveLength(2);
    expect(container.textContent).not.toMatch(/###|1\. Metformin/);
    expect(screen.getByText("Your medicines")).toBeInTheDocument();
  });

  it("splits grouped citations", () => {
    expect(normalizeAnswer("LDL is high [1, 3].")).toBe("LDL is high [1][3].");
  });

  it("leaves ordinary text alone", () => {
    const text = "Take 2 tablets at 8:00 [1]. Ask about it on Monday.";
    expect(normalizeAnswer(text)).toBe(text);
  });
});
