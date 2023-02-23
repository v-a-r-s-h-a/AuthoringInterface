// import {
//   Button,
//   Center,
//   Heading,
//   Image,
//   Spinner,
//   Table,
//   Tbody,
//   Td,
//   Th,
//   Thead,
//   Tr
// } from "@chakra-ui/react";
// import axios from "axios";
// import { useEffect, useMemo, useState } from "react";
// import { useTable, useSortBy } from "react-table";
// const url = "https://fakestoreapi.com/products";

// const tableColumn = [
//   {
//     Header: "Not Yet Changed",
//     columns: [
//       {
//         Header: "ID",
//         accessor: "id",
//       },
//       {
//         Header: "Title",
//         accessor: "title",
//       },
//       {
//         Header: "Category",
//         accessor: "category",
//       },
//     ],
//   },
//   {
//     Header: "Changed",
//     columns: [
//       {
//         Header: "Product Image",
//         accessor: "image",
//         Cell: ({ row }) => <Image src={row.values.image} h={100} />,
//       },
//       {
//         Header: "Price",
//         accessor: "price",
//         Cell: ({ row }) => ` $${row.values.price}`,
//       },
//       {
//         Header: "Action",
//         accessor: "action",
//         Cell: ({ row }) => (
//           <Button size="sm" onClick={() => alert(`$${row.values.price}`)}>
//             Show Price
//           </Button>
//         ),
//       },
//     ],
//   },
// ];

// const Test = () => {
//   const [products, setProducts] = useState([]);
//   const columns = useMemo(() => tableColumn, []);
//   const data = useMemo(() => products, [products]);
//   const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } =
//     useTable(
//       {
//         columns,
//         data,
//       },
//       useSortBy
//     );
//   useEffect(() => {
//     const fetchProducts = async () => {
//       try {
//         const { data } = await axios.get(url);
//         setProducts(data);
//       } catch (error) {
//         console.log(error);
//       }
//     };
//     fetchProducts();
//   }, []);
//   console.log(products);

//   if (products.length === 0)
//     return (
//       <Center>
//         <Spinner />
//       </Center>
//     );

//   return (
//     <>
//       <Heading>React Table </Heading>
//       <Table variant="striped" colorScheme="orange" {...getTableProps()}>
//         <Thead>
//           {headerGroups.map((headerGroup) => (
//             <Tr {...headerGroup.getHeaderGroupProps()}>
//               {headerGroup.headers.map((column) => (
//                 <Th {...column.getHeaderProps(column.getSortByToggleProps())}>
//                   {column.render("Header")}
//                   {column.isSorted ? (column.isSortedDesc ? " 🔽" : " 🔼") : ""}
//                   {}
//                 </Th>
//               ))}
//             </Tr>
//           ))}
//         </Thead>
//         <Tbody {...getTableBodyProps()}>
//           {rows.map((row, i) => {
//             prepareRow(row);

//             return (
//               <Tr {...row.getRowProps()}>
//                 {row.cells.map((cell) => (
//                   <Td {...cell.getCellProps()}>{cell.render("Cell")}</Td>
//                 ))}
//               </Tr>
//             );
//           })}
//         </Tbody>
//       </Table>
//     </>
//   );
// };

// export default Test;

import React from "react";
import Button from "@material-ui/core/Button";
import { useTheme } from "@material-ui/core/styles";
import KeyboardArrowRight from "@material-ui/icons/KeyboardArrowRight";
import KeyboardArrowLeft from "@material-ui/icons/KeyboardArrowLeft";
import MobileStepper from "@material-ui/core/MobileStepper";

const Test = () => {
    const theme = useTheme();

    const forwardButton = () => {
        setActiveStep((prevActiveStep) => prevActiveStep - 1);
    };

    const [INDEX, setActiveStep] = React.useState(0);

    const previousButton = () => {
        setActiveStep((prevActiveStep) => prevActiveStep + 1);
    };

    return (
        <div
            style={{
                marginLeft: "40%",
            }}
        >
            <h2>How to Show Pagination in ReactJS?</h2>
            <MobileStepper
                steps={5}
                variant="dots"
                style={{
                    flexGrow: 1,
                    maxWidth: 400,
                }}
                activeStep={INDEX}
                position="static"
                nextButton={
                    <Button size="small"
                        onClick={previousButton}
                        disabled={INDEX === 4}>
                        Next
                        {theme.direction !== "rtl" ? (
                            <KeyboardArrowRight />
                        ) : (
                            <KeyboardArrowLeft />
                        )}
                    </Button>
                }
                backButton={
                    <Button size="small"
                        onClick={forwardButton}
                        disabled={INDEX === 0}>
                        {theme.direction !== "rtl" ? (
                            <KeyboardArrowLeft />
                        ) : (
                            <KeyboardArrowRight />
                        )}
                        Back
                    </Button>
                }
            />
            <h3>Page No: {INDEX + 1}</h3>
        </div>
    );
};

export default Test;
