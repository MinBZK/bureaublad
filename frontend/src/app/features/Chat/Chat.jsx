"use client";
import React, { useState, useEffect } from "react";

import { Avatar, List } from "antd";
import { WechatOutlined } from "@ant-design/icons";
import Link from "next/link";
import Widget from "@/app/Common/Widget";
import moment from "moment";

function Chat() {
  const [chat, setChat] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  useEffect(() => {
    setLoading(true);
    const fetchChat = async () => {
      try {
        const res = await axios.get(`${baseUrl}/api/v1/chat/rooms`);
        setChat(res.data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchChat();
  }, []);

  const items = data?.map((value) => ({
    key: value?.id,
    label: value?.title,
    children: (
      <List
        dataSource={value?.messages}
        renderItem={(msg) => <List.Item key={msg.id}>{msg.content}</List.Item>}
      />
    ),
  }));
  return (
    <Widget title="Chat" loading={loading} error={false}>
      <List
        dataSource={data}
        renderItem={(item) => (
          <List.Item key={item.id}>
            <List.Item.Meta
              title={<Link href="/#">{item.title}</Link>}
              description={<span>Gemaakt op:{moment(item?.created_at).format("DD-MM-yyyy HH:mm")}</span>}
            />
            <Link href="/#">
              <Avatar
                style={{ backgroundColor: "#1677ff" }}
                icon={<WechatOutlined />}
              />
            </Link>
          </List.Item>
        )}
      />
    </Widget>
  );
}

export default Chat;

const data = [
  {
    id: "d8aab747-ac69-44ce-8f78-cbd2c01f0490",
    title: "test",
    created_at: "2025-10-15T07:29:03.000225Z",
    updated_at: "2025-10-15T07:29:07.921359Z",
    messages: [
      {
        id: "42ee48cf-712c-4947-b348-55b9036de746",
        createdAt: "2025-10-15T07:29:03.127445Z",
        content: "test",
        reasoning: null,
        experimental_attachments: null,
        role: "user",
        annotations: null,
        toolInvocations: null,
        parts: [{ type: "text", text: "test" }],
      },
      {
        id: "a2785781-ae0a-4d9c-9643-181ca6936810",
        createdAt: "2025-10-15T07:29:07.919195Z",
        content:
          "It seems like you're just testing our connection. If you have any questions or need help with something, feel free to ask! \n\n### Available Assistance\nI can assist with a wide range of topics, including but not limited to:\n- Answering questions on various subjects\n- Providing explanations and examples\n- Helping with basic math problems (just format your math notation between `$$` like `$$2 + 2$$`)\n- Offering suggestions and ideas\n\nLet me know how I can help you today!",
        reasoning: null,
        experimental_attachments: null,
        role: "assistant",
        annotations: null,
        toolInvocations: null,
        parts: [
          {
            type: "text",
            text: "It seems like you're just testing our connection. If you have any questions or need help with something, feel free to ask! \n\n### Available Assistance\nI can assist with a wide range of topics, including but not limited to:\n- Answering questions on various subjects\n- Providing explanations and examples\n- Helping with basic math problems (just format your math notation between `$$` like `$$2 + 2$$`)\n- Offering suggestions and ideas\n\nLet me know how I can help you today!",
          },
        ],
      },
    ],
  },
  {
    id: "8c8a4867-b707-4d0a-9cc5-114a694c7c3ess",
    title: "Hoe versla je microsoft ms365",
    created_at: "2025-10-14T12:11:07.536846Z",
    updated_at: "2025-10-14T12:11:38.540341Z",
    messages: [
      {
        id: "c1a3556f-93fe-427a-bf1d-2cbbb85466d2",
        createdAt: "2025-10-14T12:11:08.328907Z",
        content: "Hoe versla je microsoft ms365",
        reasoning: null,
        experimental_attachments: null,
        role: "user",
        annotations: null,
        toolInvocations: null,
        parts: [
          {
            type: "text",
            text: "Hoe versla je microsoft ms365",
          },
        ],
      },
      {
        id: "00802024-daa3-4f28-80f4-636811d2c82c",
        createdAt: "2025-10-14T12:11:38.524974Z",
        content:
          "Een interessante vraag! Microsoft MS365 is een krachtige suite van productiviteitssoftware, maar het is zeker mogelijk om een autonome oplossing te creëren die soortgelijke functionaliteiten biedt. Hier zijn enkele stappen die je kunt nemen om een autonome oplossing te ontwikkelen die concurrerend is met MS365:\n\n### 1. **Definieer je doelen en vereisten**\nVoordat je begint, moet je duidelijk hebben wat je wilt bereiken met je autonome oplossing. Welke functionaliteiten van MS365 wil je repliceren? Wil je een volledige suite ontwikkelen of je focussen op specifieke onderdelen zoals e-mail, documentbeheer of projectmanagement?\n\n### 2. **Kies een platform en technologie**\nJe moet beslissen welk platform en welke technologieën je wilt gebruiken voor je autonome oplossing. Dit kan variëren van open-source software tot proprietary oplossingen. Enkele opties zijn:\n- **Open-source**: Zoals LibreOffice voor documentbeheer, Thunderbird voor e-mail en Nextcloud voor cloudopslag en -synchronisatie.\n- **Self-hosted oplossingen**: Zoals Mastodon voor sociale netwerken, Matrix voor communicatie en OnlyOffice voor documentbeheer.\n\n### 3. **Ontwikkel een ecosysteem**\nEen autonome oplossing moet een ecosysteem zijn dat verschillende diensten en functionaliteiten integreert. Dit kan inhouden:\n- **Documentbeheer**: Een platform voor het maken, delen en bewerken van documenten.\n- **E-mail en communicatie**: Een e-mailclient en mogelijkheden voor internettelefonie en videoconferencing.\n- **Projectmanagement**: Tools voor het plannen, organiseren en volgen van projecten.\n- **Opslag en synchronisatie**: Een cloudopslagoplossing die bestanden synchroniseert over apparaten.\n\n### 4. **Beveiliging en privacy**\nBeveiliging en privacy zijn essentieel voor elke autonome oplossing. Zorg ervoor dat je sterke encryptie implementeert, toegangscontrole en dat je gebruikersgegevens respecteert en beschermt.\n\n### 5. **Gebruiksvriendelijkheid**\nZorg ervoor dat je oplossing gebruiksvriendelijk is. Een intuïtieve interface en een lage drempel voor adoptie zijn cruciaal voor de acceptatie van je autonome oplossing.\n\n### 6. **Community en ondersteuning**\nBouw een community rond je oplossing. Dit kan helpen bij het vinden van bugs, het voorstellen van nieuwe functionaliteiten en het bieden van ondersteuning aan gebruikers.\n\n### 7. **Itereer en verbeter**\nLuister naar feedback van gebruikers en blijf je oplossing verbeteren. Voeg nieuwe functionaliteiten toe, fix bugs en zorg ervoor dat je oplossing up-to-date blijft met de laatste technologieën en trends.\n\n### Voorbeeld van een autonome oplossing\nEen voorbeeld van een autonome oplossing die concurrerend is met MS365 kan zijn:\n- **Documentbeheer**: LibreOffice of OnlyOffice\n- **E-mail**: Thunderbird of een self-hosted e-mailoplossing\n- **Cloudopslag**: Nextcloud\n- **Projectmanagement**: OpenProject of Taiga.io\n- **Communicatie**: Matrix of Mastodon\n\nDoor deze stappen te volgen en een combinatie van open-source en self-hosted oplossingen te gebruiken, kun je een krachtige autonome oplossing creëren die concurrerend is met MS365. Het is een uitdaging, maar met de juiste benadering en ondersteuning van een community, is het zeker mogelijk.",
        reasoning: null,
        experimental_attachments: null,
        role: "assistant",
        annotations: null,
        toolInvocations: null,
        parts: [
          {
            type: "text",
            text: "Een interessante vraag! Microsoft MS365 is een krachtige suite van productiviteitssoftware, maar het is zeker mogelijk om een autonome oplossing te creëren die soortgelijke functionaliteiten biedt. Hier zijn enkele stappen die je kunt nemen om een autonome oplossing te ontwikkelen die concurrerend is met MS365:\n\n### 1. **Definieer je doelen en vereisten**\nVoordat je begint, moet je duidelijk hebben wat je wilt bereiken met je autonome oplossing. Welke functionaliteiten van MS365 wil je repliceren? Wil je een volledige suite ontwikkelen of je focussen op specifieke onderdelen zoals e-mail, documentbeheer of projectmanagement?\n\n### 2. **Kies een platform en technologie**\nJe moet beslissen welk platform en welke technologieën je wilt gebruiken voor je autonome oplossing. Dit kan variëren van open-source software tot proprietary oplossingen. Enkele opties zijn:\n- **Open-source**: Zoals LibreOffice voor documentbeheer, Thunderbird voor e-mail en Nextcloud voor cloudopslag en -synchronisatie.\n- **Self-hosted oplossingen**: Zoals Mastodon voor sociale netwerken, Matrix voor communicatie en OnlyOffice voor documentbeheer.\n\n### 3. **Ontwikkel een ecosysteem**\nEen autonome oplossing moet een ecosysteem zijn dat verschillende diensten en functionaliteiten integreert. Dit kan inhouden:\n- **Documentbeheer**: Een platform voor het maken, delen en bewerken van documenten.\n- **E-mail en communicatie**: Een e-mailclient en mogelijkheden voor internettelefonie en videoconferencing.\n- **Projectmanagement**: Tools voor het plannen, organiseren en volgen van projecten.\n- **Opslag en synchronisatie**: Een cloudopslagoplossing die bestanden synchroniseert over apparaten.\n\n### 4. **Beveiliging en privacy**\nBeveiliging en privacy zijn essentieel voor elke autonome oplossing. Zorg ervoor dat je sterke encryptie implementeert, toegangscontrole en dat je gebruikersgegevens respecteert en beschermt.\n\n### 5. **Gebruiksvriendelijkheid**\nZorg ervoor dat je oplossing gebruiksvriendelijk is. Een intuïtieve interface en een lage drempel voor adoptie zijn cruciaal voor de acceptatie van je autonome oplossing.\n\n### 6. **Community en ondersteuning**\nBouw een community rond je oplossing. Dit kan helpen bij het vinden van bugs, het voorstellen van nieuwe functionaliteiten en het bieden van ondersteuning aan gebruikers.\n\n### 7. **Itereer en verbeter**\nLuister naar feedback van gebruikers en blijf je oplossing verbeteren. Voeg nieuwe functionaliteiten toe, fix bugs en zorg ervoor dat je oplossing up-to-date blijft met de laatste technologieën en trends.\n\n### Voorbeeld van een autonome oplossing\nEen voorbeeld van een autonome oplossing die concurrerend is met MS365 kan zijn:\n- **Documentbeheer**: LibreOffice of OnlyOffice\n- **E-mail**: Thunderbird of een self-hosted e-mailoplossing\n- **Cloudopslag**: Nextcloud\n- **Projectmanagement**: OpenProject of Taiga.io\n- **Communicatie**: Matrix of Mastodon\n\nDoor deze stappen te volgen en een combinatie van open-source en self-hosted oplossingen te gebruiken, kun je een krachtige autonome oplossing creëren die concurrerend is met MS365. Het is een uitdaging, maar met de juiste benadering en ondersteuning van een community, is het zeker mogelijk.",
          },
        ],
      },
    ],
  },
  {
    id: "8c8a4867-b707-4d0a-9cc5-114a694c7c3e",
    title: "Hoe versla je microsoft ms365",
    created_at: "2025-10-14T12:11:07.536846Z",
    updated_at: "2025-10-14T12:11:38.540341Z",
    messages: [
      {
        id: "c1a3556f-93fe-427a-bf1d-2cbbb85466d2",
        createdAt: "2025-10-14T12:11:08.328907Z",
        content: "Hoe versla je microsoft ms365",
        reasoning: null,
        experimental_attachments: null,
        role: "user",
        annotations: null,
        toolInvocations: null,
        parts: [
          {
            type: "text",
            text: "Hoe versla je microsoft ms365",
          },
        ],
      },
      {
        id: "00802024-daa3-4f28-80f4-636811d2c82c",
        createdAt: "2025-10-14T12:11:38.524974Z",
        content:
          "Een interessante vraag! Microsoft MS365 is een krachtige suite van productiviteitssoftware, maar het is zeker mogelijk om een autonome oplossing te creëren die soortgelijke functionaliteiten biedt. Hier zijn enkele stappen die je kunt nemen om een autonome oplossing te ontwikkelen die concurrerend is met MS365:\n\n### 1. **Definieer je doelen en vereisten**\nVoordat je begint, moet je duidelijk hebben wat je wilt bereiken met je autonome oplossing. Welke functionaliteiten van MS365 wil je repliceren? Wil je een volledige suite ontwikkelen of je focussen op specifieke onderdelen zoals e-mail, documentbeheer of projectmanagement?\n\n### 2. **Kies een platform en technologie**\nJe moet beslissen welk platform en welke technologieën je wilt gebruiken voor je autonome oplossing. Dit kan variëren van open-source software tot proprietary oplossingen. Enkele opties zijn:\n- **Open-source**: Zoals LibreOffice voor documentbeheer, Thunderbird voor e-mail en Nextcloud voor cloudopslag en -synchronisatie.\n- **Self-hosted oplossingen**: Zoals Mastodon voor sociale netwerken, Matrix voor communicatie en OnlyOffice voor documentbeheer.\n\n### 3. **Ontwikkel een ecosysteem**\nEen autonome oplossing moet een ecosysteem zijn dat verschillende diensten en functionaliteiten integreert. Dit kan inhouden:\n- **Documentbeheer**: Een platform voor het maken, delen en bewerken van documenten.\n- **E-mail en communicatie**: Een e-mailclient en mogelijkheden voor internettelefonie en videoconferencing.\n- **Projectmanagement**: Tools voor het plannen, organiseren en volgen van projecten.\n- **Opslag en synchronisatie**: Een cloudopslagoplossing die bestanden synchroniseert over apparaten.\n\n### 4. **Beveiliging en privacy**\nBeveiliging en privacy zijn essentieel voor elke autonome oplossing. Zorg ervoor dat je sterke encryptie implementeert, toegangscontrole en dat je gebruikersgegevens respecteert en beschermt.\n\n### 5. **Gebruiksvriendelijkheid**\nZorg ervoor dat je oplossing gebruiksvriendelijk is. Een intuïtieve interface en een lage drempel voor adoptie zijn cruciaal voor de acceptatie van je autonome oplossing.\n\n### 6. **Community en ondersteuning**\nBouw een community rond je oplossing. Dit kan helpen bij het vinden van bugs, het voorstellen van nieuwe functionaliteiten en het bieden van ondersteuning aan gebruikers.\n\n### 7. **Itereer en verbeter**\nLuister naar feedback van gebruikers en blijf je oplossing verbeteren. Voeg nieuwe functionaliteiten toe, fix bugs en zorg ervoor dat je oplossing up-to-date blijft met de laatste technologieën en trends.\n\n### Voorbeeld van een autonome oplossing\nEen voorbeeld van een autonome oplossing die concurrerend is met MS365 kan zijn:\n- **Documentbeheer**: LibreOffice of OnlyOffice\n- **E-mail**: Thunderbird of een self-hosted e-mailoplossing\n- **Cloudopslag**: Nextcloud\n- **Projectmanagement**: OpenProject of Taiga.io\n- **Communicatie**: Matrix of Mastodon\n\nDoor deze stappen te volgen en een combinatie van open-source en self-hosted oplossingen te gebruiken, kun je een krachtige autonome oplossing creëren die concurrerend is met MS365. Het is een uitdaging, maar met de juiste benadering en ondersteuning van een community, is het zeker mogelijk.",
        reasoning: null,
        experimental_attachments: null,
        role: "assistant",
        annotations: null,
        toolInvocations: null,
        parts: [
          {
            type: "text",
            text: "Een interessante vraag! Microsoft MS365 is een krachtige suite van productiviteitssoftware, maar het is zeker mogelijk om een autonome oplossing te creëren die soortgelijke functionaliteiten biedt. Hier zijn enkele stappen die je kunt nemen om een autonome oplossing te ontwikkelen die concurrerend is met MS365:\n\n### 1. **Definieer je doelen en vereisten**\nVoordat je begint, moet je duidelijk hebben wat je wilt bereiken met je autonome oplossing. Welke functionaliteiten van MS365 wil je repliceren? Wil je een volledige suite ontwikkelen of je focussen op specifieke onderdelen zoals e-mail, documentbeheer of projectmanagement?\n\n### 2. **Kies een platform en technologie**\nJe moet beslissen welk platform en welke technologieën je wilt gebruiken voor je autonome oplossing. Dit kan variëren van open-source software tot proprietary oplossingen. Enkele opties zijn:\n- **Open-source**: Zoals LibreOffice voor documentbeheer, Thunderbird voor e-mail en Nextcloud voor cloudopslag en -synchronisatie.\n- **Self-hosted oplossingen**: Zoals Mastodon voor sociale netwerken, Matrix voor communicatie en OnlyOffice voor documentbeheer.\n\n### 3. **Ontwikkel een ecosysteem**\nEen autonome oplossing moet een ecosysteem zijn dat verschillende diensten en functionaliteiten integreert. Dit kan inhouden:\n- **Documentbeheer**: Een platform voor het maken, delen en bewerken van documenten.\n- **E-mail en communicatie**: Een e-mailclient en mogelijkheden voor internettelefonie en videoconferencing.\n- **Projectmanagement**: Tools voor het plannen, organiseren en volgen van projecten.\n- **Opslag en synchronisatie**: Een cloudopslagoplossing die bestanden synchroniseert over apparaten.\n\n### 4. **Beveiliging en privacy**\nBeveiliging en privacy zijn essentieel voor elke autonome oplossing. Zorg ervoor dat je sterke encryptie implementeert, toegangscontrole en dat je gebruikersgegevens respecteert en beschermt.\n\n### 5. **Gebruiksvriendelijkheid**\nZorg ervoor dat je oplossing gebruiksvriendelijk is. Een intuïtieve interface en een lage drempel voor adoptie zijn cruciaal voor de acceptatie van je autonome oplossing.\n\n### 6. **Community en ondersteuning**\nBouw een community rond je oplossing. Dit kan helpen bij het vinden van bugs, het voorstellen van nieuwe functionaliteiten en het bieden van ondersteuning aan gebruikers.\n\n### 7. **Itereer en verbeter**\nLuister naar feedback van gebruikers en blijf je oplossing verbeteren. Voeg nieuwe functionaliteiten toe, fix bugs en zorg ervoor dat je oplossing up-to-date blijft met de laatste technologieën en trends.\n\n### Voorbeeld van een autonome oplossing\nEen voorbeeld van een autonome oplossing die concurrerend is met MS365 kan zijn:\n- **Documentbeheer**: LibreOffice of OnlyOffice\n- **E-mail**: Thunderbird of een self-hosted e-mailoplossing\n- **Cloudopslag**: Nextcloud\n- **Projectmanagement**: OpenProject of Taiga.io\n- **Communicatie**: Matrix of Mastodon\n\nDoor deze stappen te volgen en een combinatie van open-source en self-hosted oplossingen te gebruiken, kun je een krachtige autonome oplossing creëren die concurrerend is met MS365. Het is een uitdaging, maar met de juiste benadering en ondersteuning van een community, is het zeker mogelijk.",
          },
        ],
      },
    ],
  },
];
