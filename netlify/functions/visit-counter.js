// netlify/functions/visit-counter.js
exports.handler = async function(event, context) {
  try {
    const namespace = 'beamindia';
    const key = 'site';
    const url = `https://api.countapi.xyz/hit/${namespace}/${key}`;
    const response = await fetch(url);
    const data = await response.json();
    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' },
      body: JSON.stringify({ count: data.value || 0 })
    };
  } catch (e) {
    return { statusCode: 200, headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ count: 0 }) };
  }
};
