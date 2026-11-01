// n8n Code node: Run Once for All Items. No external dependencies.
const text = value => typeof value === 'string' ? value.trim() : '';
return $input.all().map((item, index) => {
  const body = item.json?.body;
  const source = body && typeof body === 'object' && !Array.isArray(body) ? body : {};
  const eventId = text(source.eventId);
  const name = text(source.name);
  const email = text(source.email).toLowerCase();
  const errors = [];
  if (!/^[a-zA-Z0-9_-]{1,100}$/.test(eventId)) errors.push('eventId must contain 1-100 letters, numbers, underscores or hyphens');
  if (name.length < 2 || name.length > 100) errors.push('name must contain 2-100 characters');
  if (email.length > 254 || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) errors.push('email is invalid');
  const valid = errors.length === 0;
  return {
    json: {
      statusCode: valid ? 200 : 422,
      response: valid
        ? { valid: true, persisted: false, lead: { eventId, name, email } }
        : { valid: false, errors }
    },
    pairedItem: { item: index }
  };
});
