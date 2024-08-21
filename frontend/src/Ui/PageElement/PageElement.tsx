import { Paper } from "@mui/material";
import { FC, ReactNode } from "react";

interface IPageElement {
	children: ReactNode;
}

const PageElement: FC<IPageElement> = ({ children }) => {
	return (
		<Paper
			sx={{ "border-radius": "8px", padding: "15px", boxShadow: "none" }}
			elevation={7}
		>
			{children}
		</Paper>
	);
};

export default PageElement;
