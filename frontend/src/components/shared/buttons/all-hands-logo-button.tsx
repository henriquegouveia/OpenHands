import AllHandsLogo from "#/assets/branding/aisembly-logo.svg?react";
import { TooltipButton } from "./tooltip-button";

interface AllHandsLogoButtonProps {
  onClick: () => void;
}

export function AllHandsLogoButton({ onClick }: AllHandsLogoButtonProps) {
  return (
    <TooltipButton
      tooltip="AIsembly"
      ariaLabel="AIsembly Logo"
      onClick={onClick}
    >
      <AllHandsLogo width={32} height={32} />
    </TooltipButton>
  );
}
