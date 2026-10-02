import { createContext, useContext } from "react";

export const SearchContext = createContext({ openSearch: () => {} });

export function useSearchPalette() {
  return useContext(SearchContext);
}
