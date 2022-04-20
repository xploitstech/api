import React from "react";
import { Skeleton, Container } from "@chakra-ui/react";
import {
  Table,
  Th,
  Tr,
  Thead,
  Tbody,
  Button,
  useMediaQuery,
  Accordion,
  AccordionItem,
  AccordionButton,
  AccordionPanel,
  AccordionIcon,
  Box,
} from "@chakra-ui/react";
import { useSubscriptions } from "../core/hooks";
import SubscriptionCard from "./SubscriptionCard";

const SubscriptionsList = ({ emptyCTA }) => {
  const [isLargerThan530px] = useMediaQuery(["(min-width: 530px)"]);
  const { subscriptionsCache, subscriptionTypeIcons } = useSubscriptions();

  const cellProps = {
    px: ["16px", "8px", "16px"],
  };

  if (
    subscriptionsCache.data &&
    subscriptionsCache.data.subscriptions.length > 0
  ) {
    return (
      <>
        {isLargerThan530px && (
          <Table
            borderColor="gray.200"
            borderWidth="1px"
            variant="simple"
            colorScheme="blue"
            justifyContent="center"
            borderBottomRadius="xl"
            alignItems="baseline"
            h="auto"
            size="sm"
            mt={0}
          >
            <Thead>
              <Tr>
                <Th {...cellProps}>Token</Th>
                <Th {...cellProps}>Label</Th>
                <Th {...cellProps}>Address</Th>
                <Th {...cellProps}>abi</Th>
                <Th {...cellProps}>Color</Th>
                <Th {...cellProps}>Date Created</Th>
                <Th {...cellProps}>Actions</Th>
              </Tr>
            </Thead>

            <Tbody>
              {subscriptionsCache.data.subscriptions.map((subscription) => {
                const iconLink =
                  subscriptionTypeIcons[subscription.subscription_type_id];
                return (
                  <SubscriptionCard
                    key={`token-row-${subscription.id}`}
                    subscription={subscription}
                    isDesktopView={isLargerThan530px}
                    iconLink={iconLink}
                  />
                );
              })}
            </Tbody>
          </Table>
        )}
        {!isLargerThan530px && (
          <Accordion allowToggle={true}>
            {subscriptionsCache.data.subscriptions.map((subscription) => {
              const iconLink =
                subscriptionTypeIcons[subscription.subscription_type_id];
              return (
                <SubscriptionCard
                  key={`token-row-${subscription.id}`}
                  subscription={subscription}
                  isDesktopView={isLargerThan530px}
                  iconLink={iconLink}
                />
              );
            })}

            <AccordionItem>
              <h2>
                <AccordionButton>
                  <Box flex="1" textAlign="left">
                    Section 2 title
                  </Box>
                  <AccordionIcon />
                </AccordionButton>
              </h2>
              <AccordionPanel pb={4}>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
                eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut
                enim ad minim veniam, quis nostrud exercitation ullamco laboris
                nisi ut aliquip ex ea commodo consequat.
              </AccordionPanel>
            </AccordionItem>
          </Accordion>
        )}
      </>
    );
  } else if (
    subscriptionsCache.data &&
    subscriptionsCache.data.subscriptions.length === 0
  ) {
    return (
      <Container>
        {` You don't have any subscriptions at the moment.`}
        {emptyCTA && <Button variant="green">Create one</Button>}
      </Container>
    );
  } else if (subscriptionsCache.isLoading) {
    return <Skeleton />;
  } else {
    return "";
  }
};
export default SubscriptionsList;
