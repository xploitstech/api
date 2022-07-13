import React from "react";
// import { MODAL_TYPES } from "../core/providers/OverlayProvider/constants";
import { Flex, Heading } from "@chakra-ui/react";
import showdown from "showdown";
import showdownHighlight from "showdown-highlight";

const ExampleCode = () => {
  const converter = new showdown.Converter({
    ghCompatibleHeaderId: true,
    parseImgDimensions: true,
    simplifiedAutoLink: true,
    literalMidWordUnderscores: true,
    strikethrough: true,
    tables: true,
    tasklists: true,
    openLinksInNewWindow: true,
    emoji: true,
    smartIndentationFix: true,
    extensions: [showdownHighlight({ pre: true })],
    disableForced4SpacesIndentedSublists: true,
    ghCodeBlocks: true,
  });
  const code = `
    \`\`\`js
    async function startRandomLootboxOpening(lootboxId) {
    let userAddress = window.ethereum.selectedAddress;
        \tlet activeOpening = await checkUsersActiveLootboxOpeningStatus(userAddress);
        if (activeOpening != null) {
            console.log("User already has active opening");
            return;
        }

        const count = 1; // you can open only 1 random lootbox at a time
        await openOrdinaryLootbox(lootboxId, count);
    }
    \`\`\`
  `;
  let formattedCode = converter.makeHtml(code);
  console.log(formattedCode);

  const HtmlCode = () => {
    return (
      <>
        <pre className="js language-js">
          <code className="hljs js language-js">
            <span className="hljs-keyword">{"async"}</span>{" "}
            <span className="hljs-function">
              <span className="hljs-keyword">function</span>{" "}
              <span className="hljs-title">startRandomLootboxOpening</span>
              {"("}
              <span className="hljs-params">lootboxId</span>
              {")"}{" "}
            </span>
            {"{"}
            <br />
            &nbsp; &nbsp;
            <span className="hljs-keyword">{"let"}</span> {"userAddress ="}{" "}
            <span className="hljs-built_in">{"window"}</span>
            {".ethereum.selectedAddress;"}
            <br />
            &nbsp; &nbsp;
            <span className="hljs-keyword">{"let"}</span> activeOpening ={" "}
            <span className="hljs-keyword">{"await"}</span>{" "}
            {"checkUsersActiveLootboxOpeningStatus(userAddress);"}
            <br />
            &nbsp; &nbsp;
            <span className="hljs-keyword">{"if"}</span> (activeOpening !={" "}
            <span className="hljs-literal">null</span>
            {") {"}
            <br />
            &nbsp; &nbsp; &nbsp; &nbsp;
            <span className="hljs-built_in">{"console"}</span>
            {".log"}(
            <span className="hljs-string">
              &quot;User already has active opening&quot;
            </span>
            {");"}
            <br />
            &nbsp; &nbsp; &nbsp; &nbsp;
            <span className="hljs-keyword">{"return"}</span>; <br />
            &nbsp; &nbsp;
            {"}"}
            <br />
            &nbsp; &nbsp;
            <span className="hljs-keyword">const</span> count ={" "}
            <span className="hljs-number">1</span>;{" "}
            <span className="hljs-comment">
              {"// you can open only 1 random lootbox at a time"}
            </span>
            <br />
            &nbsp; &nbsp;
            <span className="hljs-keyword">await</span>{" "}
            openOrdinaryLootbox(lootboxId, count);
            <br />
            {"}"}
          </code>
        </pre>
      </>
    );
  };

  return (
    <Flex
      // h={["auto", "auto", "320px"]}
      flexDirection="column"
      textColor="white"
      bgColor="#686464"
      p="20px"
      rounded="lg"
    >
      <Heading as="h3" fontSize="lg" pb="20px">
        We make sure our code is easy to use. Here’s an example:
      </Heading>
      {/* <Flex dangerouslySetInnerHTML={formattedCode}></Flex> */}
      {/* <Flex>{formattedCode}</Flex> */}
      <Flex position={"relative"}>
        <HtmlCode />
      </Flex>
      {/* <Text fontSize="md">
        {"async function startRandomLootboxOpening( lootboxId ) {"}
      </Text>
      <Text fontSize="md">
        {" "}
        &nbsp; &nbsp;
        {"let userAddress = window.ethereum.selectedAddress;"}
      </Text>
      <Text fontSize="md">
        {" "}
        &nbsp; &nbsp;
        {
          "let activeOpening = await checkUsersActiveLootboxOpeningStatus( userAddress );"
        }
      </Text>
      <Text fontSize="md">&nbsp; &nbsp;{"if ( activeOpening != null ) {"}</Text>
      <Text fontSize="md">
        &nbsp; &nbsp; &nbsp; &nbsp;
        {"console.log('User already has active opening');"}
      </Text>
      <Text fontSize="md">&nbsp; &nbsp; &nbsp; &nbsp;{"return;"}</Text>
      <Text fontSize="md">&nbsp; &nbsp;{"}"}</Text>
      <Text fontSize="md">
        &nbsp; &nbsp;
        {"const count = 1; // you can open only 1 random lootbox at a time"}
      </Text>
      <Text fontSize="md">
        &nbsp; &nbsp;{"await openOrdinaryLootbox( lootboxId, count );"}
      </Text>
      <Text fontSize="md">{"}"}</Text> */}
    </Flex>
  );
};

export default ExampleCode;
