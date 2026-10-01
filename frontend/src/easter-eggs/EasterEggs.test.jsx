import { describe, expect, it, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { EasterEggProvider, useEasterEggs } from "./EasterEggs";

vi.mock("sonner", () => ({ toast: vi.fn() }));

function Found() {
  const { found } = useEasterEggs();
  return <p>found:{found.join(",")}</p>;
}

describe("easter eggs", () => {
  it("discovers the 'apple' egg when the word is typed outside inputs", async () => {
    localStorage.clear();
    render(
      <EasterEggProvider>
        <Found />
        <input aria-label="field" />
      </EasterEggProvider>,
    );
    await userEvent.type(screen.getByLabelText("field"), "apple");
    expect(screen.getByText("found:")).toBeInTheDocument();

    screen.getByLabelText("field").blur();
    await userEvent.keyboard("apple");
    expect(await screen.findByText("found:apple")).toBeInTheDocument();
  });
});
